import cv2 as cv
from cv2.typing import MatLike
from .scanner import image_scaner

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
    def __init__(self, id, image_og: MatLike, resize_factor = 0.15):
        self.id = id
        
        self.img_og = image_og

        
        self.img_resized = self.resize_2_std(image_og, resize_factor)
        
       
        w, h = self.img_resized.shape[:2]
        self.img_scan = self.resize_2_std(image_scaner(self.img_resized), 1, w, w)

        #self.show_steps()

    def resize_2_std(self, img, factor, w= None, h = None):
        """
        ### Resize image
        Resizes image to a standard size

        #### Args:  
        img: image to be resized

        #### Returns:
        Resized image
        """
        if w == None and h == None:
            w, h = img.shape[:2]

        resized_image = cv.resize(img, (int(w*factor), int(h*factor)), interpolation=cv.INTER_LINEAR)
        
        return resized_image


    def show_steps(self):

        cv.imshow('resized', self.img_resized)
        cv.imshow('scanned', self.img_scan)
        cv.waitKey(0)
        cv.destroyAllWindows()


