from objs import Grid, GridImageNormalizer, ImageLoader, ColorContourExtractor
from backend import identify_block

import cv2 as cv

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

        ## display
        im = image.copy()
        im = cv.resize(im, (0,0), fx=0.5, fy=0.5)
        cv.imshow('image', im)
        cv.waitKey(0)
        cv.destroyAllWindows()

        #   Create Image object from loaded image.
        # The Image object is used to store the image 
        # and the steps of the image processing.
        image_scan, id = GridImageNormalizer.scan(id, image, 1)
        if image_scan is None: continue

        ## display
        im = cv.resize(image_scan, (0,0), fx=0.5, fy=0.5)
        cv.imshow('image', im)
        cv.waitKey(0)
        cv.destroyAllWindows()

        #   Finds the contours around non-grayscale (colorful) 
        # edges in image. The contours are used to find the 
        # pins and later blocks.
        contours = ColorContourExtractor.process_image(image_scan)

        ## display
        im = image_scan.copy()
        for contour in contours:
            cv.drawContours(im, [contour], 0, (0,255,0), 3)
        cv.imshow('image', im)
        cv.waitKey(0)
        cv.destroyAllWindows()

        #   Create Grid object from the scanned image. The grid
        # is used to store information about the grid, such as 
        # the blocks and pins, etc.
        Grid_DS = Grid(image_scan)

        ## display
        im = Grid_DS.img.copy()
        Grid_DS.draw_gridLines(im)
        cv.imshow('image', im)
        cv.waitKey(0)
        cv.destroyAllWindows()


        # determines what squares in grid are blocks
        Grid_DS.find_blocks(contours); print(f"there are {len(Grid_DS.blocks)} blocks in the grid")

        ## display
        im = Grid_DS.img.copy()
        Grid_DS.draw_blocks(im)
        cv.imshow('image', im)
        cv.waitKey(0)



        # identifies type of blocks in the grid
        for block in Grid_DS.blocks:
            block.get_raw_sequence()
            identify_block(block)

if __name__ == '__main__':
    path_to_imgs =  r"data\New_images_022624\IMG_5513.JPEG"
    main(path_to_imgs)



"""
TODO:
change raw_sequence to rgb_sequence

TODO:
add reference to scan

TODO: 
image generation with blocks for U-NET

TODO:
write on saved image the identified block types, and the sequence of the block

TODO:
make a block class that inherits from the square class
"""