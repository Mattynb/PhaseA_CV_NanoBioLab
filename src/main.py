from objs import Grid
from backend import identify_block
from objs import Image, ImageLoader, ImageProcessor


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

    # loading images from given path
    images = ImageLoader.load_images(path_to_imgs)
    id = 0
    # Analyzing each image
    for image in images:

        #   Create Image object from loaded image.
        # The Image object is used to store the image 
        # and the steps of the image processing.
        image_scan, id = Image.scan(id, image, 1)
        if image_scan is None: continue


        #   Finds the contours around non-grayscale (colorful) 
        # edges in image. The contours are used to find the 
        # pins and later blocks.
        contours = ImageProcessor.process_image(image_scan)


        #   Create Grid object from the scanned image. The grid
        # is used to store information about the grid, such as 
        # the blocks and pins, etc.
        Grid_DS = Grid(image_scan); #Grid_DS.show_gridLines()


        # determines what squares in grid are blocks
        Grid_DS.find_blocks(contours)
        print(f"there are {len(Grid_DS.blocks)} blocks in the grid")

        # identifies type of blocks in the grid
        for block in Grid_DS.blocks:
            block.get_raw_sequence()
            identify_block(block)


if __name__ == '__main__':
    path_to_imgs =  r"data\New_images_022624\IMG_5513.JPEG"
    main(path_to_imgs)

"""
TODO: 
image generation with blocks for U-NET
"""