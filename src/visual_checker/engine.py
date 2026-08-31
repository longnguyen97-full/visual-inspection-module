import time
from typing import Union, Tuple, Optional
from pathlib import Path
import numpy as np
from PIL import Image

from .core.preprocessor import ImagePreprocessor
from .core.comparator import ImageComparator
from .core.morphology import MorphologyProcessor
from .core.detector import DefectDetector
from .formatters.prompt_builder import PromptBuilder
from .schemas.report import VisualInspectionResult

class VisualInspectionEngine:
    """
    Main Facade Engine for Visual Regression Inspection.
    Integrates Preprocessing -> Diff Computation -> Morphology -> Contour Detection -> Report Generation.
    """

    def __init__(
        self,
        ssim_threshold: float = 0.995,
        diff_threshold_val: int = 25,
        min_defect_area: int = 40,
        filter_noise: bool = False
    ):
        self.ssim_threshold = ssim_threshold
        self.diff_threshold_val = diff_threshold_val
        self.min_defect_area = min_defect_area
        self.filter_noise = filter_noise

    def compare(
        self,
        baseline_input: Union[str, Path, bytes, np.ndarray, Image.Image],
        current_input: Union[str, Path, bytes, np.ndarray, Image.Image]
    ) -> Tuple[VisualInspectionResult, np.ndarray, np.ndarray]:
        """
        Executes full inspection pipeline.
        Returns:
            result: VisualInspectionResult (Pydantic model)
            annotated_image: np.ndarray (Current image with red bounding boxes)
            diff_heatmap: np.ndarray (Color heatmap overlay)
        """
        start_time = time.perf_counter()

        # 1. Load images
        img_baseline = ImagePreprocessor.load_image(baseline_input)
        img_current = ImagePreprocessor.load_image(current_input)

        # 2. Harmonize dimensions
        img_baseline, img_current = ImagePreprocessor.align_dimensions(img_baseline, img_current)

        base_proc = ImagePreprocessor.filter_noise(img_baseline) if self.filter_noise else img_baseline
        curr_proc = ImagePreprocessor.filter_noise(img_current) if self.filter_noise else img_current

        # 3. Diff Analysis (SSIM + Channel-wise Pixel Diff)
        ssim_score, ssim_diff_map = ImageComparator.compute_ssim(base_proc, curr_proc)
        pixel_diff = ImageComparator.compute_pixel_diff(base_proc, curr_proc)

        # Combined diff map
        combined_diff = np.maximum(ssim_diff_map, pixel_diff)

        # 4. Morphology
        thresh_mask = MorphologyProcessor.threshold_diff(combined_diff, thresh_val=self.diff_threshold_val)
        clustered_mask = MorphologyProcessor.cluster_regions(thresh_mask, kernel_size=9, iterations=2)

        # 5. Extract Contours & Bounding Boxes
        defects = DefectDetector.extract_defect_regions(
            clustered_mask,
            min_area=self.min_defect_area,
            img_shape=img_current.shape[:2]
        )

        total_pixels = img_current.shape[0] * img_current.shape[1]
        diff_pixels = int(np.count_nonzero(thresh_mask))
        diff_ratio = diff_pixels / total_pixels

        # Defect condition: any validated region with significant diff pixels
        has_defect = (len(defects) > 0) or (diff_pixels >= self.min_defect_area) or (ssim_score < self.ssim_threshold)

        # 6. Render Overlays
        annotated_image = DefectDetector.draw_defect_boxes(img_current, defects if has_defect else [])
        diff_heatmap = ImageComparator.create_heatmap_overlay(img_current, combined_diff)

        exec_time_ms = (time.perf_counter() - start_time) * 1000.0

        # 7. Build LLM Agent Summary
        summary = PromptBuilder.build_summary(
            has_defect=has_defect,
            ssim_score=ssim_score,
            diff_ratio=diff_ratio,
            defects=defects if has_defect else []
        )

        result = VisualInspectionResult(
            has_defect=has_defect,
            ssim_score=round(ssim_score, 4),
            diff_pixel_ratio=round(diff_ratio, 5),
            defect_count=len(defects) if has_defect else 0,
            defects=defects if has_defect else [],
            agent_prompt_summary=summary,
            execution_time_ms=round(exec_time_ms, 2)
        )

        return result, annotated_image, diff_heatmap
