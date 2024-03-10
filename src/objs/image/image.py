import cv2 as cv
from numpy import ndarray
from .image_scanner import ImageScanner

class GridImageNormalizer:
    """
    ### Image Normalizer
    Class to normalize the image of the grid by scanning the grid and making it square ratio.

    #### Methods:
    - `scan(id: int, image: ndarray, resize_factor: float = 1) -> (Image, int)`
        - This method scans the image and returns the scanned image.
    - `resize_2_std(img: ndarray, factor: float, w:int=None, h:int = None) -> ndarray`
        - This method resizes the image to a given percentage of the current size.
    """
    @classmethod
    def scan(cls, id: int, image: ndarray, resize_factor : float = 1):
        """
        ### Scan image
        Scan the image and return the scanned image.

        #### Args:
        * id : id of the image
        * image : image to be scanned
        * resize_factor : percentage of current size to resize to

        #### Returns:
        * scanned image
        """
        print(f"Image {id} loaded")

        # Scan the image isolating the grid
        Image_i = ImageScanner.scan(image); id += 1; print(f"Image {id} scanned!\n")

        # Resize image so that its height and width are the same
        Image_i = cls.resize(Image_i, resize_factor)

        return Image_i, id

    @staticmethod
    def resize(img: ndarray, factor: float, w:int=None, h:int = None):
        """
        ### Resize
        Resize image to a given percentage of current size.

        #### Args:
        * img : image to be resized
        * factor : percentage of current size to resize to
        * w : width of image
        * h : height of image

        #### Returns:
        * resized image
        """

        # If width and height are not given, get them from the image
        if w == None and h == None:
            w, h = img.shape[:2]

        resized_image = cv.resize(img, (int(w*factor), int(h*factor)), interpolation=cv.INTER_CUBIC)

        return resized_image