import cv2
import numpy as np

class MorphologyProcessor:
    """Applies thresholding, dilation, and closing to cluster discrete noisy diff pixels."""

    @staticmethod
    def threshold_diff(diff_map: np.ndarray, thresh_val: int = 25) -> np.ndarray:
        """Applies binary thresholding to isolate significant discrepancies."""
        _, thresh = cv2.threshold(diff_map, thresh_val, 255, cv2.THRESH_BINARY)
        return thresh

    @staticmethod
    def cluster_regions(thresh_mask: np.ndarray, kernel_size: int = 9, iterations: int = 2) -> np.ndarray:
        """
        Applies morphological dilation and closing to merge adjacent pixel discrepancies
        (e.g., individual letters in a broken text line) into a coherent component boundary.
        """
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
        
        # 1. Closing: fill small holes inside regions
        closed = cv2.morphologyEx(thresh_mask, cv2.MORPH_CLOSE, kernel, iterations=iterations)
        
        # 2. Dilation: connect neighboring components
        dilated = cv2.dilate(closed, kernel, iterations=iterations)
        
        return dilated
