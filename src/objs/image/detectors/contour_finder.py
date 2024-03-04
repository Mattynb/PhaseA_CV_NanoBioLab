import cv2 as cv
import numpy as np

class ContourFinder:
    @staticmethod
    def find_contours(self, image: np.ndarray) -> list:
        contours, _ = cv.findContours(image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        return sorted(contours, key=cv.contourArea, reverse=True)[:5]
