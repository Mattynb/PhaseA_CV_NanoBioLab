import cv2 as cv
import numpy as np

class CornerDetector:
    """
    ## CornerDetector
    
    The `CornerDetector` class is responsible for detecting the corners of a given image given the contours.

    ### Methods
    - `detect_corners(contours: list, img: np.ndarray) -> list`
        - This method detects the corners of a given image given the contours and returns the corners.
    
    ### Example
    ```python
    import cv2 as cv
    import numpy as np
    from src.objs.image.detectors.contour_finder import ContourFinder
    from src.objs.image.detectors.corner_detector import CornerDetector
    
    image = cv.imread('path/to/image.jpg')
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    edges = cv.Canny(blurred, 50, 150)
    contours = ContourFinder.find_contours(edges)
    corners = CornerDetector.detect_corners(contours, image)
    ```
    """
    @staticmethod
    def detect_corners(contours: list, img: np.ndarray) -> list:
        """This method detects the corners of a given image given the contours and returns the corners."""

        # Loop through the contours and find the corners
        for c in contours:
            # Approximate the contour
            epsilon = 0.02 * cv.arcLength(c, True)
            
            # Get the corners of the contour using the approxPolyDP method
            corners = cv.approxPolyDP(c, epsilon, True)

            # If the contour has 4 corners, return the corners
            if len(corners) == 4:
                return sorted(np.concatenate(corners).tolist())
        
        # If no corners are found, return an empty list
        return []
