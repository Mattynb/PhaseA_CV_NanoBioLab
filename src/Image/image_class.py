import cv2 as cv
from Image.image_scanner import Image_scan
from cv2.typing import MatLike

class Image:
    """
    ### Image class
    ---------------
    Class that contains all the information of an image

    #### Attributes:
    ---------------
    * id : image id (int)
    * img_og : original image (MatLike) 
    * img_std_size : resized image (MatLike)
    * img_std : scanned image (MatLike)

    #### Methods:
    ---------------
    pre_process()
        work in progress
    
    resize_2_std(img, factor=0.25)
        Resizes image to a standard size
    """
    def __init__(self, id = int, image_og = MatLike):
        self.id = id
        
        self.img_og = image_og
        self.img_std_size = self.resize_2_std(image_og)
        
        self.img_std = Image_scan(self.img_std_size)

        #self.img_std = self.pre_process()  # std == processed
        """ The pins are the only part of the image that isnt "black" or "white".
        Therefore you could potentially look for the colored pins by looking for the pixels that arent black or white threshold.
        e.g if pixel rgb avg value is > 10 and < 245 then its a pin"""

    def pre_process(self):
        """ work in progress """
        ...

        return 

    
    def resize_2_std(self, img, factor=0.25):
        """
        ### Resize image
        Resizes image to a standard size

        #### Args:  
        img: image to be resized

        #### Returns:
        Resized image
        """

        h, w = img.shape[:2]
        return cv.resize(img, (int(w*factor), int(h*factor)), interpolation=cv.INTER_LINEAR)





