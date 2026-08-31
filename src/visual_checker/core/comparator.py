from typing import Tuple
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

class ImageComparator:
    """Computes Structural Similarity Index (SSIM) and Pixel-by-Pixel Difference."""

    @staticmethod
    def compute_ssim(img1: np.ndarray, img2: np.ndarray) -> Tuple[float, np.ndarray]:
        """
        Computes multi-channel SSIM or grayscale SSIM between two BGR images.
        """
        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        score, diff = ssim(gray1, gray2, full=True)
        # diff in range [-1.0, 1.0] -> convert to [0, 255]
        diff_map = ((1.0 - diff) * 127.5).astype(np.uint8)
        return float(score), diff_map

    @staticmethod
    def compute_pixel_diff(img1: np.ndarray, img2: np.ndarray) -> np.ndarray:
        """
        Computes maximum absolute color difference across all BGR channels.
        Ensures high sensitivity to color mutations (e.g. Yellow -> Red).
        """
        abs_diff = cv2.absdiff(img1, img2)
        # Max across channels gives true color contrast
        max_diff = np.max(abs_diff, axis=2)
        return max_diff

    @staticmethod
    def create_heatmap_overlay(base_image: np.ndarray, diff_mask: np.ndarray, alpha: float = 0.5) -> np.ndarray:
        """Creates a colorized heatmap overlay on the base image."""
        heatmap = cv2.applyColorMap(diff_mask, cv2.COLORMAP_JET)
        indices = diff_mask > 20
        overlay = base_image.copy()
        overlay[indices] = cv2.addWeighted(base_image, 1 - alpha, heatmap, alpha, 0)[indices]
        return overlay
