from Image.image_class import Image
from Image.image_loader import Image_load

from Image.image_preprocess import pre_process, adaptive_pre_process, grid


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
    Images = []
    for img in images_og:
        try:
            Images.append(Image(id, img, 0.4))
            print(f"Image {id} loaded")
            id += 1
        except AttributeError:
            print("\nImage not loaded, check path\n")

    # finding pins
    for img in Images:
        grid(img.img_scan)

if __name__ == '__main__':
    path_to_imgs = r"C:\Users\Matheus\Desktop\NanoTechnologies_Lab\Phase A\data\grid_on_black_img\std_angle\IMG_5011.JPEG" #data\grid_on_black_img\std_angle\
    main(path_to_imgs)






            




