import cv2 as cv
import numpy as np

class ImageProcessor:
    def process_image(self, image: np.ndarray) -> np.ndarray:
        raise NotImplementedError
