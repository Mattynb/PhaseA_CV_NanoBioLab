import cv2 as cv
import numpy as np

class GPUMorphologicalTransformer():
    """
    ## reference
    https://learnopencv.com/automatic-document-scanner-using-opencv/
    """
    @staticmethod
    def apply_morph(gpu_img: np.ndarray) -> np.ndarray:
        """This method applies morphological transformations to the given image and returns the processed image."""

        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
        morph = cv.cuda.createMorphologyFilter(cv.MORPH_OPEN, gpu_img.type(), kernel, iterations=3)
        gpu_img = morph.apply(gpu_img)

        return gpu_img
