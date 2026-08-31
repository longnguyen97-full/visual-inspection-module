from typing import List, Tuple
import cv2
import numpy as np
from ..schemas.report import BoundingBox, DefectRegion

class DefectDetector:
    """Extracts bounding contours, filters noise, and classifies severity."""

    @staticmethod
    def extract_defect_regions(
        processed_mask: np.ndarray,
        min_area: int = 50,
        img_shape: Tuple[int, int] = (800, 1000)
    ) -> List[DefectRegion]:
        """
        Finds contours in binary mask and constructs DefectRegion models.
        """
        contours, _ = cv2.findContours(processed_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        regions: List[DefectRegion] = []
        img_h, img_w = img_shape[:2]
        total_img_area = img_h * img_w
        
        defect_idx = 1
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < min_area:
                continue
            
            x, y, w, h = cv2.boundingRect(cnt)
            bbox = BoundingBox(x=x, y=y, width=w, height=h)
            
            # Severity classification
            area_ratio = bbox.area / total_img_area
            if area_ratio > 0.05 or w > 300 or h > 200:
                severity = "critical"
            elif area_ratio > 0.01 or w > 100 or h > 80:
                severity = "warning"
            else:
                severity = "minor"
                
            # Region layout heuristic
            if y < img_h * 0.15:
                region_type = "header"
            elif y > img_h * 0.85:
                region_type = "footer"
            else:
                region_type = "main_content"
                
            regions.append(DefectRegion(
                id=defect_idx,
                bbox=bbox,
                area=int(area),
                severity=severity,
                region_type=region_type
            ))
            defect_idx += 1
            
        return regions

    @staticmethod
    def draw_defect_boxes(
        image: np.ndarray,
        defects: List[DefectRegion],
        box_color: Tuple[int, int, int] = (0, 0, 255),  # Red in BGR
        thickness: int = 2
    ) -> np.ndarray:
        """Annotates the image with bounding boxes and defect labels."""
        annotated = image.copy()
        for defect in defects:
            b = defect.bbox
            x1, y1 = b.x, b.y
            x2, y2 = b.x + b.width, b.y + b.height
            
            # Draw rectangle
            cv2.rectangle(annotated, (x1, y1), (x2, y2), box_color, thickness)
            
            # Draw badge label
            label = f"Defect #{defect.id} [{defect.severity.upper()}]"
            font = cv2.FONT_HERSHEY_SIMPLEX
            scale = 0.5
            thick = 1
            (text_w, text_h), baseline = cv2.getTextSize(label, font, scale, thick)
            
            # Label background box
            label_y1 = max(0, y1 - text_h - 8)
            label_y2 = y1
            cv2.rectangle(annotated, (x1, label_y1), (x1 + text_w + 10, label_y2), box_color, -1)
            cv2.putText(annotated, label, (x1 + 5, label_y2 - 4), font, scale, (255, 255, 255), thick, cv2.LINE_AA)
            
        return annotated
