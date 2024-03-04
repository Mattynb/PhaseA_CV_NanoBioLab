import cv2 as cv
import numpy as np

class CornerDetector:
    def detect_corners(self, contours: list, img: np.ndarray) -> list:
        for c in contours:
            epsilon = 0.02 * cv.arcLength(c, True)
            corners = cv.approxPolyDP(c, epsilon, True)
            if len(corners) == 4:
                return sorted(np.concatenate(corners).tolist())
        return []
