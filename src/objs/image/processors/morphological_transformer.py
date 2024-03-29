import cv2 as cv
import numpy as np

class MorphologicalTransformer():
    """
    ## reference
    https://learnopencv.com/automatic-document-scanner-using-opencv/
    """
    @staticmethod
    def apply_morph(img: np.ndarray) -> np.ndarray:
        """This method applies morphological transformations to the given image and returns the processed image."""

        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
        morph_img = cv.morphologyEx(img, cv.MORPH_OPEN, kernel, iterations=3)

        return morph_img
