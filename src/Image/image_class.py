import cv2 as cv
from cv2.typing import MatLike
from random import randint
from Image.image_scanner import Image_scan

#from Image.image_preprocess import pre_process

class Image:
    """
    ### Image class
    ---------------
    Class that contains all the information of an image

    #### Attributes:
    ---------------
    * id : image id (int)
    * img_og : original image (MatLike) 
    * img_resized : resized image (MatLike)
    * img_std : scanned image (MatLike)

    #### Methods:
    ---------------
    pre_process()
        work in progress
    
    resize_2_std(img, factor=0.25)
        Resizes image to a standard size
    """
    def __init__(self, id = randint(0, 100), image_og = MatLike, resize_factor = 0.15):
        self.id = id
        
        self.img_og = image_og
        self.img_resized = self.resize_2_std(image_og, resize_factor)
        self.img_scan = Image_scan(self.img_resized)
        
        #self.img_std = pre_process(self.img_scan)


       
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





