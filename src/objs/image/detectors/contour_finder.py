import cv2 as cv
import numpy as np

class ContourFinder:
    """
    ## ContourFinder
    This class is responsible for finding contours in an image.

    ### Methods
    - `find_contours(image: np.ndarray) -> list`
        - This method finds the contours in the given image and returns the top 5 contours sorted by area.

    ### Example
    ```python
    import cv2 as cv
    from src.objs.image.detectors.contour_finder import ContourFinder

    image = cv.imread('path/to/image.jpg')
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0)
    edged = cv.Canny(blurred, 50, 150)
    contours = ContourFinder.find_contours(edged)
    ```
    """
    @staticmethod
    def find_contours(img: np.ndarray)->list:
        """ This method finds the contours in the given image and returns the top 5 contours sorted by area."""
        # EDGE DETECTION

        # GPU PROCESSING
        gpu_img = cv.cuda.GpuMat()
        gpu_img.upload(img)
        gpu_img = cv.cuda.cvtColor(gpu_img, cv.COLOR_BGR2GRAY)
        
        # Detecting edges using Canny edge detection
        gpu_blurred = cv.cuda.createGaussianFilter(gpu_img.type(), -1, (11, 11), 0).apply(gpu_img)
        detector = cv.cuda.createCannyEdgeDetector(0, 200)
        gpu_canny = detector.detect(gpu_blurred)

        canny_cpu = gpu_canny.download()  # Downloading for CPU processing

        # CONTOUR DETECTION (CPU)
        contours, _ = cv.findContours(canny_cpu, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        return sorted(contours, key=cv.contourArea, reverse=True)[:5]
