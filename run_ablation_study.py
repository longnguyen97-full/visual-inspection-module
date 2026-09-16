import sys
import json
import time
from pathlib import Path
import numpy as np
import cv2

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

WORKSPACE_DIR = ROOT_DIR.parent
DATASET_DIR = WORKSPACE_DIR / "dataset"

from visual_checker.core.preprocessor import ImagePreprocessor
from visual_checker.core.comparator import ImageComparator
from visual_checker.core.morphology import MorphologyProcessor
from visual_checker.core.detector import DefectDetector

def run_ablation():
    configs = [
        {"name": "1. Raw Grayscale Diff", "mode": "raw_gray"},
        {"name": "2. SSIM Only", "mode": "ssim_only"},
        {"name": "3. Max Color Diff Only", "mode": "color_only"},
        {"name": "4. SSIM + Color (No Morphology)", "mode": "no_morph"},
        {"name": "5. Full Proposed Pipeline", "mode": "full_pipeline"}
    ]
    
    # Load dataset pairs
    s1_pairs = []
    for i in range(1, 26):
        fn = f"sample_{i:02d}.png"
        b = DATASET_DIR / "scenario_1" / "baseline" / fn
        c = DATASET_DIR / "scenario_1" / "current" / fn
        s1_pairs.append((b, c, False)) # Ground truth: No defect
        
    s2_pairs = []
    for i in range(1, 26):
        fn = f"sample_{i:02d}.png"
        b = DATASET_DIR / "scenario_2" / "baseline" / fn
        c = DATASET_DIR / "scenario_2" / "current" / fn
        s2_pairs.append((b, c, True)) # Ground truth: Has defect
        
    all_pairs = s1_pairs + s2_pairs
    
    summary_results = []
    
    for cfg in configs:
        mode = cfg["mode"]
        tp, fp, tn, fn = 0, 0, 0, 0
        total_time = 0.0
        avg_boxes = []
        
        for b_path, c_path, gt_defect in all_pairs:
            t0 = time.perf_counter()
            
            img_b = ImagePreprocessor.load_image(b_path)
            img_c = ImagePreprocessor.load_image(c_path)
            img_b, img_c = ImagePreprocessor.align_dimensions(img_b, img_c)
            
            num_boxes = 0
            pred_defect = False
            
            if mode == "raw_gray":
                # Convert to grayscale, diff, threshold at 25
                gray_b = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)
                gray_c = cv2.cvtColor(img_c, cv2.COLOR_BGR2GRAY)
                diff = cv2.absdiff(gray_b, gray_c)
                _, mask = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                valid_boxes = [c for c in contours if cv2.contourArea(c) >= 40]
                num_boxes = len(valid_boxes)
                pred_defect = (num_boxes > 0) or (np.count_nonzero(mask) >= 40)
                
            elif mode == "ssim_only":
                # SSIM only
                ssim_score, ssim_diff_map = ImageComparator.compute_ssim(img_b, img_c)
                mask = MorphologyProcessor.threshold_diff(ssim_diff_map, thresh_val=25)
                clustered = MorphologyProcessor.cluster_regions(mask, kernel_size=9, iterations=2)
                contours, _ = cv2.findContours(clustered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                valid_boxes = [c for c in contours if cv2.contourArea(c) >= 40]
                num_boxes = len(valid_boxes)
                pred_defect = (ssim_score < 0.995) or (num_boxes > 0)
                
            elif mode == "color_only":
                # Max Color Diff only
                pixel_diff = ImageComparator.compute_pixel_diff(img_b, img_c)
                mask = MorphologyProcessor.threshold_diff(pixel_diff, thresh_val=25)
                clustered = MorphologyProcessor.cluster_regions(mask, kernel_size=9, iterations=2)
                contours, _ = cv2.findContours(clustered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                valid_boxes = [c for c in contours if cv2.contourArea(c) >= 40]
                num_boxes = len(valid_boxes)
                pred_defect = (num_boxes > 0) or (np.count_nonzero(mask) >= 40)
                
            elif mode == "no_morph":
                # Combined diff without morphology
                ssim_score, ssim_diff_map = ImageComparator.compute_ssim(img_b, img_c)
                pixel_diff = ImageComparator.compute_pixel_diff(img_b, img_c)
                comb = np.maximum(ssim_diff_map, pixel_diff)
                mask = MorphologyProcessor.threshold_diff(comb, thresh_val=25)
                # NO cluster_regions!
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                valid_boxes = [c for c in contours if cv2.contourArea(c) >= 40]
                num_boxes = len(valid_boxes)
                pred_defect = (ssim_score < 0.995) or (num_boxes > 0) or (np.count_nonzero(mask) >= 40)
                
            elif mode == "full_pipeline":
                # Full pipeline
                ssim_score, ssim_diff_map = ImageComparator.compute_ssim(img_b, img_c)
                pixel_diff = ImageComparator.compute_pixel_diff(img_b, img_c)
                comb = np.maximum(ssim_diff_map, pixel_diff)
                mask = MorphologyProcessor.threshold_diff(comb, thresh_val=25)
                clustered = MorphologyProcessor.cluster_regions(mask, kernel_size=9, iterations=2)
                defects = DefectDetector.extract_defect_regions(clustered, min_area=40, img_shape=img_c.shape[:2])
                num_boxes = len(defects)
                pred_defect = (ssim_score < 0.995) or (num_boxes > 0) or (np.count_nonzero(mask) >= 40)
                
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            total_time += elapsed_ms
            
            if gt_defect:
                if pred_defect:
                    tp += 1
                else:
                    fn += 1
                avg_boxes.append(num_boxes)
            else:
                if pred_defect:
                    fp += 1
                else:
                    tn += 1
                    
        total = tp + tn + fp + fn
        acc = (tp + tn) / total if total else 0
        prec = tp / (tp + fp) if (tp + fp) else 0
        rec = tp / (tp + fn) if (tp + fn) else 0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) else 0
        fpr = fp / (fp + tn) if (fp + tn) else 0
        avg_box_count = np.mean(avg_boxes) if avg_boxes else 0
        avg_latency = total_time / len(all_pairs)
        
        summary_results.append({
            "Config": cfg["name"],
            "Accuracy": acc,
            "Precision": prec,
            "Recall": rec,
            "F1": f1,
            "FPR": fpr,
            "Avg_BBoxes_per_Defect": round(avg_box_count, 2),
            "Latency_ms": round(avg_latency, 1)
        })
        
    print(json.dumps(summary_results, indent=2))

if __name__ == "__main__":
    run_ablation()
