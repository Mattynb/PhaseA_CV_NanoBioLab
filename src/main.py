from image import Image, image_loader, pre_process
from objs import Grid

from backend import identify_blocks

def main(path_to_imgs):
    """
    ### Main function
    Loads all the images in a folder and creates an Image object for each image.

    #### Args:
    path_to_imgs: path to image folder
    """

    # loading images
    original_images = image_loader(path_to_imgs)

    # creating Image objects
    id = 0
    for img in original_images:
        try:
            Image_i = Image(id, img, 0.3)
            print(f"Image {id} loaded")
            id += 1
        
        except AttributeError:
            print("\nImage not loaded, check path\n")
            break

        Grid_DS = Grid(Image_i.img_scan); Grid_DS.show_gridLines()
        
        contours = pre_process(Image_i.img_scan)
        Grid_DS.find_blocks(contours)

        identify_blocks(Grid_DS)
        

if __name__ == '__main__':
    path_to_imgs =  r"C:\Users\Matheus\Desktop\NanoTechnologies_Lab\Phase A\data\grid_wit_block_A_B\IMG_5190.jpeg"    #IMG_5020.JPEG
    main(path_to_imgs)


"""
TODO:
Fix the index of grid to be (row, col) instead of (col, row)

TODO:
implement the __init__.py (aka index.js) file for every folder

TODO:
Apply SOLID

TODO: 
Add a descriptive pre_precess function that shows all the steps using the currently commented code in the pre_process function.

"""