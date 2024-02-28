from tracemalloc import start
from image import Image, image_loader, pre_process
from objs import Grid
import time
from backend import identify_block

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

    start = time.time()
    # loading image files in a way we can use
    original_images = image_loader(path_to_imgs)
    end = time.time()
    #print(f"Time to load images: {end - start} seconds")

    # creating an Image object, Grid object, and finding blocks for each image
    id = 0
    for img in original_images:
        try:
            # Create Image object from loaded image
            start = time.time()
            Image_i = Image(id, img, 0.35); print(f"Image {id} loaded")
            id += 1
            end = time.time()
            #print(f"Time to create Image object: {round(end - start,2)} seconds")

        except AttributeError:
            # if the image is not loading
            print("\nImage not loaded, check path\n")
            continue

        
        # creating a grid object with the scanned image
        start = time.time()
        Grid_DS = Grid(Image_i.img_scan); #Grid_DS.show_gridLines()
        end = time.time()
        #print(f"Time to create Grid object: {round(end - start,2)} seconds")

        # finds the contours around non-grayscale (colorful) edges in image
        start = time.time()
        contours = pre_process(Image_i.img_scan)
        end = time.time()
        #print(f"Time to find contours: {round(end - start,2)} seconds")

        # determines what squares in grid are blocks
        start = time.time()
        Grid_DS.find_blocks(contours)
        end = time.time()
        print(f"Time to find blocks: {round(end - start,2)} seconds")

        print(f"there are {len(Grid_DS.blocks)} blocks in the grid")
        # identifies type of blocks in the grid
        for block in Grid_DS.blocks:
            block.get_raw_sequence()
            identify_block(block)
        

if __name__ == '__main__':
    path_to_imgs =  r"data\New_images_022624\IMG_5514.JPEG" #"C:\Users\Matheus\Desktop\NanoTechnologies_Lab\Phase A\data\img_5356"    #IMG_5020.JPEG
    main(path_to_imgs)

    #path_new = r"C:\Users\Matheus\Desktop\NanoTechnologies_Lab\Phase A\data\grid_on_black_img\std_angle\IMG_5020.jpeg" 
    #main(path_new)
    
    

   


"""
TODO:
Image normalization HSV?

TODO: 
image generation with blocks for U-NET (find out what that is)

TODO: 
Add a descriptive pre_precess function that shows all the steps using the currently commented code in the pre_process function.
"""