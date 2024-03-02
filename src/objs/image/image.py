import cv2 as cv
from numpy import ndarray
from .image_scanner import ImageScanner

import time
class Image:
    @classmethod
    def scan(cls, id: int, image: ndarray, resize_factor : float = 1):
        """
        ### Image maker
        Create Image object from loaded image.

        #### Args:
        * id : id of the image
        * image : loaded image
        * resize_factor : percentage of current size to resize to

        #### Returns:
        * Image object | None
        * id
        """

        # Create Image object from loaded image
        t = time.time()
        Image_i = ImageScanner.scan(image); id += 1; print(f"Image {id} loaded")
        print(f"Processing time: {time.time() - t} seconds")

        # Resize image to a given percentage of current size
        Image_i = cls.resize_2_std(Image_i, resize_factor)
        
        return Image_i, id

    @staticmethod
    def resize_2_std(img: ndarray, factor: float, w:int=None, h:int = None):
        """
        ### Resize image
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