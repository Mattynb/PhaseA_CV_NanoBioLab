from image import Image, image_loader, pre_process
from objs import Grid

from backend import identify_blocks

def main(path_to_imgs):
    """
    ### Main function
    ---------------
    Main function of the program. Loads the images, creates the Image objects, and finds the blocks in the image.

    #### Args:
    path_to_imgs: path to images to be loaded

    #### Returns:
    None
    """

    # loading image files in a way we can use
    original_images = image_loader(path_to_imgs)

    # creating an Image object, Grid object, and finding blocks for each image
    id = 0
    for img in original_images:
        try:
            # Create Image object from loaded image
            Image_i = Image(id, img, 0.5); print(f"Image {id} loaded")
            id += 1

        except AttributeError:
            # if the image is not loading
            print("\nImage not loaded, check path\n")
            continue


        # creating a grid object with the scanned image
        Grid_DS = Grid(Image_i.img_scan); #Grid_DS.show_gridLines()


        # finds the contours around non-grayscale (colorful) edges in image
        contours = pre_process(Image_i.img_scan)


        # determines what squares in grid are blocks
        Grid_DS.find_blocks(contours)


        # identifies type of blocks in the grid
        #identify_blocks(Grid_DS)
        

if __name__ == '__main__':
    path_to_imgs =  r"C:\Users\Matheus\Desktop\NanoTechnologies_Lab\Phase A\data\grid_wit_block_A_B\IMG_5190.jpeg"    #IMG_5020.JPEG
    main(path_to_imgs)

    #path_new = r"C:\Users\Matheus\Desktop\NanoTechnologies_Lab\Phase A\data\grid_on_black_img\std_angle\IMG_5020.jpeg" 
    #main(path_new)
    
    

   


"""

TODO:
Image normalization HSV?

TODO:
"database" of block ids 

TODO: 
image generation with blocks for U-NET (find out what that is)

TODO: 
Add a descriptive pre_precess function that shows all the steps using the currently commented code in the pre_process function.

"""