import cv2 as cv
import numpy as np

class PerspectiveTransformer:
    @staticmethod
    def apply_transform(cls, img: np.ndarray, corners: list) -> np.ndarray:
        destination_corners = cls.calculate_destination_corners(corners)
        M = cv.getPerspectiveTransform(np.float32(corners), np.float32(destination_corners))
        transformed_image = cv.warpPerspective(img, M, (destination_corners[2][0], destination_corners[2][1]), flags=cv.INTER_LINEAR)
        return transformed_image
    
    @classmethod
    def calculate_destination_corners(cls, corners: list)->list:
        # DESTINATION COORDINATES
        (tl, tr, br, bl) = corners

        # Finding the maximum width.
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        # Finding the maximum height.
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        # Final destination co-ordinates.
        destination_corners = [[0, 0], [maxWidth, 0], [maxWidth, maxHeight], [0, maxHeight]]
        return cls.order_points(destination_corners)