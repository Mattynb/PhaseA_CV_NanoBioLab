from PIL import Image as im
from glob import glob
import pillow_heif
import cv2 as cv


class ImageLoader:
    """
    ## ImageLoader
    
    This class is responsible for loading images from a given folder and converting HEIC images to JPG.
    
    ### Methods
    - `load_images(path_to_imgs: str) -> list`
        - This method loads all the images in a folder and returns a list of images.
    - `heic2jpg(path_to_heic: str) -> None`
        - This method creates .jpg images from the .HEIC images of given folder.
        
    ### Example
    ```python
    from src.objs.image.utils.image_loader import ImageLoader

    images = ImageLoader.load_images('path/to/images')
    or 
    images = ImageLoader.heic2jpg('path/to/heic')
    images = ImageLoader.load_images('path/to/images')
    ```
    """
    @staticmethod
    def load_images(path_to_imgs: str):
        """
        ### Image loader
        Loads all the images in a folder and returns a list of images
        
        #### Args:
        path_to_images: path to image folder

        #### Returns:
        List of images
        """

        # acceptable image types
        types = ('.png', '.jpg', '.jpeg', '.JPEG', '.PNG', '.JPG')

        # reading single image if path is only one image
        end = path_to_imgs[-4:]
        if end in types or end.lower() == 'jpeg': 
            return [cv.imread(path_to_imgs)]

        # reading all images of acceptable types from given directory 
        imgs = []
        for f_type in types: 
            imgs.extend([cv.imread(file) for file in glob(f"{path_to_imgs}*{f_type}")])
        
        return imgs

    @ staticmethod
    def heic2png(path_to_heic: str):
        """
        ### HEIC to PNG converte
        Creates .png images from the .HEIC images of given folder.    
        
        #### Args:
        path_to_heic: path to image folder

        #### Returns:
        None
        """
        
        # finding all .HEIC images in the given folder 
        # and converting them to .png
        paths = glob(f"{path_to_heic}.HEIC")
        for path in paths:
            pillow_heif.register_heif_opener()

            img = im.open(path)
            img.save(path[:-4] + 'png', format="png")