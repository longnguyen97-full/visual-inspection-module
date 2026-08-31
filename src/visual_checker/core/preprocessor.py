from typing import Tuple, Union
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
import io

class ImagePreprocessor:
    """Handles image loading, dimensional harmonization, and anti-aliasing noise reduction."""

    @staticmethod
    def load_image(image_input: Union[str, Path, bytes, np.ndarray, Image.Image]) -> np.ndarray:
        """Loads an image into a standard BGR numpy array."""
        if isinstance(image_input, (str, Path)):
            img = cv2.imread(str(image_input))
            if img is None:
                raise ValueError(f"Could not load image from path: {image_input}")
            return img
        elif isinstance(image_input, bytes):
            nparr = np.frombuffer(image_input, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("Could not decode image from bytes.")
            return img
        elif isinstance(image_input, Image.Image):
            rgb = np.array(image_input.convert("RGB"))
            return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        elif isinstance(image_input, np.ndarray):
            if len(image_input.shape) == 2:
                return cv2.cvtColor(image_input, cv2.COLOR_GRAY2BGR)
            return image_input.copy()
        else:
            raise TypeError(f"Unsupported image input type: {type(image_input)}")

    @staticmethod
    def align_dimensions(img1: np.ndarray, img2: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Ensures both images share identical dimensions by resizing if needed."""
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]

        if (h1, w1) == (h2, w2):
            return img1, img2

        # Target max dimensions
        target_w = max(w1, w2)
        target_h = max(h1, h2)

        aligned1 = cv2.resize(img1, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)
        aligned2 = cv2.resize(img2, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)

        return aligned1, aligned2

    @staticmethod
    def filter_noise(image: np.ndarray, filter_type: str = "gaussian") -> np.ndarray:
        """Applies light filtering to eliminate font anti-aliasing artifacts."""
        if filter_type == "gaussian":
            return cv2.GaussianBlur(image, (3, 3), 0)
        elif filter_type == "bilateral":
            return cv2.bilateralFilter(image, d=5, sigmaColor=35, sigmaSpace=35)
        return image
