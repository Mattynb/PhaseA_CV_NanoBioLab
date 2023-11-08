from os import path
from PIL import Image as im
from glob import glob
import pillow_heif
import cv2 as cv

def Image_load(path_to_images):
    """
    ### Image loader
    Loads all the images in a folder and returns a list of images
    
    #### Args:
    path_to_images: path to image folder

    #### Returns:
    List of images
    """

    types = ('.png', '.jpg', '.jpeg')

    # reading single image if path is only one image
    end = path_to_images[-4:]
    
    if end in types or end == 'jpeg': 
        return [cv.imread(path_to_images)]

    # reading all images of acceptable types from given directory 
    imgs = []
    for f_type in types: 
        imgs.extend([cv.imread(file) for file in glob(f"{path_to_images}*{f_type}")])
    
    return imgs

def heic2jpg(path_to_heic):
    """
    ### HEIC to JPG converte
    Creates .jpg images from the .HEIC images of given folder.    
    
    #### Args:
    path_to_heic: path to image folder

    #### Returns:
    None
    """

    paths = glob(f"{path_to_heic}.HEIC")

    for path in paths:
        pillow_heif.register_heif_opener()

        img = im.open(path)
        img.save(path[:-4] + 'png', format="png")