from Image.image_class import Image
from Image.image_loader import Image_load


def main(path_to_imgs):
    """
    ### Main function
    Loads all the images in a folder and creates an Image object for each image


    #### Args:
    path_to_imgs: path to image folder
    """

    images_og = Image_load(path_to_imgs)

    id = 0
    Images = []
    for img in images_og:
        try:
            Images.append(Image(id, img))
            id += 1
        except AttributeError:
            print("\nImage not loaded, check path\n")

if __name__ == '__main__':
    path_to_imgs = r"C:\Users\Matheus\Desktop\NanoTechnologies_Lab\Phase A\data\grid_on_black_img\IMG_4993.png"
    main(path_to_imgs)





            




