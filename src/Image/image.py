from math import e
from re import I
from turtle import st
import cv2 as cv
from cv2.typing import MatLike
from .scanner import image_scaner
import numpy as np
import time

class Image:
    """
    ---------------
    Class that represents an image. It contains the original image, the resized image and the scanned image.
    
    #### Args:
    * id : image id (int)
    * image_og : original image (MatLike)
    * resize_factor : factor to resize the image (float)

    #### Attributes:
    * id : image id (int)
    * img_og : original image (MatLike)
    * img_resized : resized image (MatLike)
    * img_scan : scanned image (MatLike)

    #### Methods:
    * resize_2_std : resize image to a standard size
    * show_steps : show the steps img_og -> img_resized -> img_scan
    """
    def __init__(self, id: int, image_og: MatLike, resize_factor : float = .15):
        self.id = id
        
        self.img_og = image_og  # original image

        start = time.time()
        # resizing image to fit i screen
        self.img_resized: MatLike = self.resize_2_std(image_og, resize_factor)
        end = time.time()
        #print(f"Time to resize image: {end - start} seconds")


        # scanning the grid in the image
        w, h = self.img_resized.shape[:2] 
        start = time.time()
        img_scan = self.resize_2_std(image_scaner(self.img_resized), 1, w, w)
        end = time.time()
        #print(f"Time to scan image: {end - start} seconds")

        start = time.time()
        self.img_scan = self.white_balance(img_scan)   
        end = time.time()
        #print(f"Time to white balance image: {end - start} seconds")
        #self.show_steps()

    def resize_2_std(self, img: MatLike, factor: float, w:int=None, h:int = None):
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
        if w == None and h == None:
            w, h = img.shape[:2]

        resized_image = cv.resize(img, (int(w*factor), int(h*factor)), interpolation=cv.INTER_CUBIC)
        
        return resized_image


    def show_steps(self):
        """
        ### Show steps
        Show the steps img_og -> img_resized -> img_scan
        """
        
        cv.imshow('original', self.img_og)
        cv.imshow('resized', self.img_resized)
        cv.imshow('scanned', self.img_scan)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def white_balance(self, image):

        reference_size=(20, 20)
        reference_top_left=(62, 80)

        

        # Create the reference 10x10 square for the reference region for white balancing
        reference_region = image[reference_top_left[1]:reference_top_left[1] + reference_size[1],
                                reference_top_left[0]:reference_top_left[0] + reference_size[0]]

        # Calculate the mean RGB values of the reference region - image white baseline value
        mean_reference = np.mean(reference_region, axis=(0, 1))

        # Scaling factors for each channel
        scale_factors = 255.0 / mean_reference

        # Apply white balancing to the entire image by multiplying the image to the scale factor
        balanced_image = cv.merge([cv.multiply(image[:, :, i], scale_factors[i]) for i in range(3)])

        # Clip the values to the valid range [0, 255]
        balanced_image = np.clip(balanced_image, 0, 255).astype(np.uint8)

        #cv.rectangle(balanced_image, reference_top_left, (reference_top_left[0] + reference_size[0], reference_top_left[1] + reference_size[1]), (0, 255, 0), 2)
        
        return balanced_image
        



