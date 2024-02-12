import cv2 as cv
from cv2.typing import MatLike
from .scanner import image_scaner

#from Image.image_preprocess import pre_process

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
    def __init__(self, id: int, image_og: MatLike, resize_factor : float = 1):
        self.id = id
        
        self.img_og = image_og  # original image

        # resizing image to fit in screen
        self.img_resized: MatLike = self.resize_2_std(image_og, resize_factor)
        
        # scanning the grid in the image
        w, h = self.img_resized.shape[:2] 
        self.img_scan = self.resize_2_std(image_scaner(self.img_resized), 1, w, w)

        #cv.imwrite(f"img_{self.id}_scan.jpg", self.img_scan)

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


