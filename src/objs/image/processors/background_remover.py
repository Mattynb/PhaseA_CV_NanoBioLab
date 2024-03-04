import cv2 as cv
import numpy as np


class BackgroundRemover(ImageProcessor):
    def process_image(image: np.ndarray) -> np.ndarray:
        mask = np.zeros(image.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        rect = (20, 20, image.shape[1]-20, image.shape[0]-20)
        cv.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv.GC_INIT_WITH_RECT)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        return image * mask2[:, :, np.newaxis]