import cv2 as cv
from cv2.typing import MatLike

from image import image
from .Square import Square
import itertools
from .geometry_utils import contour_is_circular, is_arranged_as_square, find_center_of_points, find_center_of_contour, xy_to_index

class Grid:
    """
    ### Grid
    ---------------
    Class that represents the grid in the image.

    #### Args:
    * img: image

    #### Attributes:
    * img: image
    * MAX_XY: max x and y coordinates of the image
    * grid: represents the grid in the image as a 2D array of squares

    ##### Experimentally Measured Ratios:
    * PIN_RATIO:     size of pin diameter/grid size
    * EDGE_RATIO:    size of edge/grid size. Edge is the "lines" around squares
    * SQUARE_RATIO:  squares are the places where you can insert the ampli blocks
    * PLUS_MINUS:    an arbitrary general tolerance
    * SQUARE_LENGTH: SQUARE_RATIO + EDGE_RATIO, used to iterate through the grid

    * MAX_INDEX:     max index of the grid_ds

    #### Methods:
    * create_grid:   creates a "map" (list of lists) of squares in the grid


    """
    def __init__(self, img: MatLike):
        # scanned image
        self.img = img.copy()

        # max x and y coordinates of the image
        self.MAX_XY = self.img.shape[0] # assumes image is square

        # ratios measured experimentally as a percentage of the grid
        self.PIN_RATIO = int(self.MAX_XY * 0.012)     # size of pin diameter/grid size
        self.EDGE_RATIO = int(self.MAX_XY * 0.01)     # size of edge/grid size. Edge is the "lines" around squares 
        self.SQUARE_RATIO = int(self.MAX_XY * 0.089)  # squares are the places where you can insert the ampli blocks
        self.PLUS_MINUS = int(self.MAX_XY * 0.005)    # an arbitrary general tolerance
        self.SQUARE_LENGTH = self.SQUARE_RATIO + self.EDGE_RATIO 

        self.MAX_INDEX = 9  # assumes grid is square 10x10 

        # represents the grid in the image as a 2D array of squares
        self.grid = self.create_grid()

        # list of blocks in the grid
        self.blocks = []
    
    # Creates a "map" (list of lists) of squares in the grid.
    def create_grid(self):
        """
        ### Create grid
        ---------------
        Function that creates a "map" (list of lists) of squares in the grid. Basically a 2D array of squares.

        #### Args:
        * None

        #### Returns:
        * grid_ds: grid object representing the grid in the image as a 2D array of squares
        """

        # First we initialize 2D array grid_ds with None values. 
        grid = [[None for _ in range(self.MAX_INDEX + 1)] for _ in range(self.MAX_INDEX + 1)]

        # Next we will replace the None values with Square objects. 
        
        # These are the stop values for the for loops.
        STOP_XY = self.MAX_XY - self.EDGE_RATIO
        STEP = self.SQUARE_LENGTH

        # iterate through the grid by moving in steps of SQUARE_LENGTH until the max x and y values are reached
        # x and y are the top left points of the squares
        # x_index and y_index are the index of the square in the grid
        for y in range(0, STOP_XY, STEP):
            for x in range(0, STOP_XY, STEP):
                
                # get the corresponding index of the square in the grid
                x_index, y_index = xy_to_index(self, x, y)

                # create a square object sq
                sq = Square(
                    # top left point
                    (x + (self.EDGE_RATIO), y + (self.EDGE_RATIO)), 
                    
                    # bottom right point
                    (x + self.SQUARE_RATIO + (self.EDGE_RATIO), y + self.SQUARE_RATIO + (self.EDGE_RATIO)),

                    # index of the square in the grid
                    (x_index, y_index),

                    # ratios
                    self.PIN_RATIO, 
                    self.PLUS_MINUS,

                    # image
                    self.img
                )
               
                # add the square to the grid list            
                grid[x_index][y_index] = sq
                

        return grid
    
    def find_blocks(self, contours: list[MatLike]):
        """
        ### Find blocks
        ---------------
        Function that determines which squares are blocks in the grid.
        It does this by finding the potential pins (p_pins) 
        then checking if the pin is in the corners of the square and adding it to the square if it is.

        #### Args:
        * contours: list of contours around non-grayscale (colorful) edges in image

        #### Returns:
        None
        """

        image_copy = self.img.copy()

        # finds the potential pins (p_pins) and adds them to their bounding squares.
        self.find_p_pins(contours)

        # checks if the potential pins are in one of the corners of square.
        # adds potential pin as a pin to the square if it is.
        for sq in itertools.chain(*self.grid):
            if len(sq.p_pins) <= 2:
                continue

            for p_pin in sq.p_pins:
                x, y, w, h = cv.boundingRect(p_pin)
                
                in_corner = False
                # checks if top left or bottom right point of pin is inside corner of square within error range
                if (sq.is_in_corners(x, y) or
                    sq.is_in_corners(x+int(w), y+int(h)) or
                    sq.is_in_corners(x-int(w), y-int(h)) or
                    sq.is_in_corners(x+int(w), y-int(h)) or
                    sq.is_in_corners(x-int(w), y+int(h))):
                    in_corner = True

                if in_corner == True: #and p_pin not in sq.pins
                    sq.add_pin(p_pin)
                    #sq.draw_pins(image_copy)
                    #self.show_gridLines(image_copy)
                    #sq.draw_corners(image_copy)
                            
        
        # checks if the square has x or more pins and if it does, it is considered a block.
        for x in self.grid:
            for sq in x:
                if len(sq.pins) > 0:
                    print(f"len(sq.pins) at index {sq.index}: {len(sq.pins)}")
                if len(sq.pins) >= 4:
                    sq.is_block = True
                    self.blocks.append(sq)

        # shows image with pins and corners drawn
        #'''
        image_copy = image_copy.copy()
        for blk in self.blocks:
            blk.draw_pins(image_copy)
            #blk.draw_corners(image_copy)
            cv.rectangle(image_copy, blk.tl, blk.br, (0,0,255), 3)

            #image_copy = cv.resize(image_copy, (800,800))
            cv.imshow('blocks', image_copy)
            cv.waitKey(0)
            cv.destroyAllWindows()
        #'''
    
    def find_p_pins(self, contours: list[MatLike]):
        """
        ### Find potential pins
        ---------------
        Function that finds the potential pins (p_pins) and adds them to their bounding squares.

        #### Args:
        * contours: list of contours around non-grayscale (colorful) edges in image
        """

        # Square structures are 4 points (in this case potential pins) arranged in the shape of a square
        square_structures, pin_list  = self.square_structures(contours)

        #"""
        img_cp = self.img.copy()
        for sq in square_structures:
            top_left = (min(sq, key=lambda x: x[0])[0], min(sq, key=lambda y: y[1])[1])
            bottom_right = (max(sq, key=lambda x: x[0])[0], max(sq, key=lambda y: y[1])[1])

            cv.rectangle(img_cp, top_left, bottom_right, (255,0,0), 3)
        
        img_cp = cv.resize(img_cp, (800,800))
        cv.imshow('blank', img_cp)
        cv.waitKey(0)
        cv.destroyAllWindows()
        #"""

        # indexes around the perimeter of grid
        top_row    = [(x, 0) for x in range(self.MAX_INDEX + 1)]
        bottom_row = [(self.MAX_INDEX, x) for x in range(self.MAX_INDEX + 1)]
        left_col   = [(0, y) for y in range(self.MAX_INDEX + 1)]
        right_col  = [(self.MAX_INDEX, y) for y in range(self.MAX_INDEX + 1)] 
        perimeter_indexes = [] + top_row + bottom_row + left_col + right_col

        # adds the 4 potential pins structured as a square shape to the square in the grid where the middle of the structure is located
        for square_structure, pins in zip(square_structures, pin_list):

            # middle of the structure 
            center = find_center_of_points(square_structure)
            x_index, y_index = xy_to_index(self, center[0], center[1])

            # p_pin contours in p_pins
            for pin in pins:
                self.grid[x_index][y_index].add_pin(pin)


    def square_structures(self, contours: list[MatLike]):
        """
        ### Square structures
        ---------------
        Function that finds the square structures in the image.  
        A square structure is defined as 4 points (in this case potential pins) arranged in the shape of a square.

        #### Args:
        * contours: list of contours around non-grayscale (colorful) edges in image

        #### Returns:
        * square_structures: list of square structures
        * p_pins: list of p_pins
        """
        square_structures = []
        pins = []

        # Find the center point of each contour
        center_to_contour_index = {}
        for i, contour in enumerate(contours):
            center = find_center_of_contour(contour)
            if center is not None:
                center_to_contour_index[center] = i

        # save the indexes bounding the centers of the contours in a list and remove None values
        centers = list(center_to_contour_index.keys()) 
        centers = [x for x in centers if x != None]

        # Find all combinations of four points      
        
        combinations = list(itertools.combinations(centers, 4))
        for comb in combinations:
            cv.destroyAllWindows()
            if is_arranged_as_square(comb, self.img, self.SQUARE_LENGTH): 

                # Add the square to the list of combinations if it is arranged as a square
                square_structures.append(list(comb))

                # Find the indices of the contours that form the square
                contour_indices = [center_to_contour_index[point] for point in comb]
                pins.append([contours[i] for i in contour_indices])


        return square_structures, pins

    
    # Appends squares to the grid.
    def append(self, x_index:int, y_index:int, square:Square):
        """ 
        appends square to grid_ds

        #### Args:
        * x_index (int): x index of square
        * y_index (int): y index of square
        * square (Square): square object
        """
        
        # checks if the square already exists at index
        if self.grid[x_index][y_index] != None:
           print('ERROR: Square already exists and is being replaced')
       
        # adds square to grid
        self.grid[x_index][y_index] = square

    # Shows the grid lines on the image.
    def show_gridLines(self, img: MatLike):
        """
        ### Show grid lines
        ---------------
        Function that shows the grid lines on the image.
        """
        
        # draw grid lines
        for i in range(0 + self.EDGE_RATIO, self.MAX_XY - self.EDGE_RATIO + self.PLUS_MINUS,  self.SQUARE_RATIO + self.EDGE_RATIO ):
            for j in range(0 + self.EDGE_RATIO, self.MAX_XY - self.EDGE_RATIO + self.PLUS_MINUS,  self.SQUARE_RATIO + self.EDGE_RATIO):

                cv.line(img, (i, 0), (i, self.MAX_XY), (0, 255, 0), 2)
                cv.line(img, (i + self.SQUARE_RATIO, 0), (i + self.SQUARE_RATIO, self.MAX_XY), (0, 255, 0), 2)

                cv.line(img, (0, i), (self.MAX_XY, i), (0, 255, 0), 2)
                cv.line(img, (0, i + self.SQUARE_RATIO), (self.MAX_XY, i + self.SQUARE_RATIO), (0, 255, 0), 2)

        """
        img = cv.resize(img.copy(), (800, 800))
        cv.imshow('grid', img)
        cv.waitKey(0)
        cv.destroyAllWindows()
        #"""