from Image.image_class import Image
from Image.image_loader import Image_load
from objs import Grid

import Image.image_preprocess as pp

def main(path_to_imgs):
    """
    ### Main function
    Loads all the images in a folder and creates an Image object for each image.

    #### Args:
    path_to_imgs: path to image folder
    """

    # loading images
    images_og = Image_load(path_to_imgs)

    # creating Image objects
    id = 0
    for img in images_og:
        try:
            Image_i = Image(id, img, 0.4)
            print(f"Image {id} loaded")
            id += 1
        
        except AttributeError:
            print("\nImage not loaded, check path\n")
            break

        Grid_DS = Grid(Image_i.img_scan)
        contours = pp.pre_process(Image_i.img_scan)
        Grid_DS.find_blocks(contours)

if __name__ == '__main__':
    path_to_imgs = r"C:\Users\Matheus\Desktop\NanoTechnologies_Lab\Phase A\data\grid_on_black_img\std_angle\IMG_5020.JPEG" #IMG_5020.JPEG
    main(path_to_imgs)

    print("next step: look at block corners for pins, get a new dataset, then encoding")





            




