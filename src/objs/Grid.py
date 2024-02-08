import cv2 as cv
from cv2.typing import MatLike
from .Square import Square

from math import sqrt 
import itertools
import numpy as np

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
        self.PIN_RATIO = round(self.MAX_XY * 0.012)     # size of pin diameter/grid size
        self.EDGE_RATIO = round(self.MAX_XY * 0.01)     # size of edge/grid size. Edge is the "lines" around squares 
        self.SQUARE_RATIO = round(self.MAX_XY * 0.089)  # squares are the places where you can insert the ampli blocks
        self.PLUS_MINUS = round(self.MAX_XY * 0.005)    # an arbitrary general tolerance
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
        for x in self.grid:
            for sq in x:
                #sq.draw_corners(image_copy)
                if len(sq.p_pins) >= 2:
                    for p_pin in sq.p_pins:
                        x, y, w, h = cv.boundingRect(p_pin)
                        
                        # checks if top left or bottom right point of pin is inside corner of square
                        if sq.is_in_corners(x, y) or sq.is_in_corners(x+int(w), y+int(h)):
                            
                            sq.add_pin(p_pin)
                            sq.draw_pins(image_copy)
                            self.show_gridLines(image_copy)
                            sq.draw_corners(image_copy)
        
        """
        cv.imshow('block', image_copy)
        cv.waitKey(0)
        cv.destroyAllWindows()
        """
                    
        # checks if the square has x or more pins and if it does, it is considered a block.
        for x in self.grid:
            for sq in x:
                if len(sq.pins) >= 4:
                    sq.is_block = True
                    sq.img = self.img
                    self.blocks.append(sq)

                    """
                    cv.imshow('block', sq.img)
                    cv.waitKey(0)
                    cv.destroyAllWindows()
                    #"""
                    
                    # outputs the rgb sequence of the pins in the block
                    # return ...
                    
                    #print(f"Square at index: {sq.index}", "{", sq.get_pins_rgb(), "}\n") 
                    #"""


        # shows image with pins and corners drawn
        #'''
        self.show_gridLines(image_copy)
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
        square_structures, p_pins  = self.square_structures(contours)

        # indexes around the perimeter of grid
        top_row    = [(x, 0) for x in range(self.MAX_INDEX + 1)]
        bottom_row = [(self.MAX_INDEX, x) for x in range(self.MAX_INDEX + 1)]
        left_col   = [(0, y) for y in range(self.MAX_INDEX + 1)]
        right_col  = [(self.MAX_INDEX, y) for y in range(self.MAX_INDEX + 1)] 
        perimeter_indexes = [] + top_row + bottom_row + left_col + right_col

        # adds the 4 potential pins structured as a square shape to the square in the grid where the middle of the structure is located
        for square_structure in square_structures:

            # middle of the structure 
            center = find_center_of_points(square_structure)
            x_index, y_index = xy_to_index(self, center[0], center[1])

            # p_pin contours in p_pins
            for combin in p_pins:
                for p_pin in combin:
                    # check curvature
                    if contour_is_circular(p_pin) or (x_index, y_index) in perimeter_indexes:

                        #print(f"\n p_pin: {len(p_pins)}x{len(p_pin[0])}x{len(p_pin[0][0])}  = {p_pin[0]}\n")
                        # add 4 pins to square
                        self.grid[x_index][y_index].add_p_pin(p_pin)


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
        p_pins = []

        # Find the center point of each contour
        center_to_contour_index = {}
        for i, contour in enumerate(contours):
            center = find_center_of_contour(contour)
            if center is not None:
                center_to_contour_index[center] = i

        # save the indexes bounding the centers of the contours in a list and remove None values
        centers = list(center_to_contour_index.keys()) 
        centers = [x for x in centers if x != None]

        # Create a blank image to draw the squares on, for visual confirmation.
        height, width, _ = self.img.shape
        blank_image = np.zeros((height,width,3), np.uint8)

        # Find all combinations of four points       
        combinations = list(itertools.combinations(centers, 4))
        for comb in combinations:
            if self.is_arranged_as_square(comb):
                
                # Add the square to the list of combinations if it is arranged as a square
                square_structures.append(list(comb))
                
                #print("Found a square:", [xy_to_index(self, x,y) for x, y in combination])

                # Find the indices of the contours that form the square
                contour_indices = [center_to_contour_index[point] for point in comb]
                p_pins.append([contours[i] for i in contour_indices])


                cv.rectangle(blank_image, comb[0], comb[3], (0, 255, 0), 1)
                cv.imshow('blank', blank_image)

        return square_structures, p_pins

    # checks if a combination of points are arranged in the shape of a square 
    def is_arranged_as_square(self, points:list[tuple]):
        """
        checks if a combination of points are arranged in the shape of a square
        ----------
        points= combination of 4 points (x,y)
        """
        
        # Assuming points is a list of four (x, y) tuples
        # Calculate distances between each pair of points
        dists = [distance(points[i], points[j]) for i in range(4) for j in range(i+1, 4)]
        dists.sort()

        # Check for four sides of equal length and two equal diagonals
        return (
            np.isclose(dists[0], dists[1], atol=0.05, rtol=0.05) 
            and np.isclose(dists[1], dists[2], atol=0.05, rtol=0.05) 
            and np.isclose(dists[2], dists[3], atol=0.05, rtol=0.05) 
            and np.isclose(dists[4], dists[5], atol=0.05, rtol=0.05)
        )
    
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
        for i in range(0 + self.EDGE_RATIO, self.MAX_XY - self.EDGE_RATIO,  self.SQUARE_RATIO + self.EDGE_RATIO):
            for j in range(0 + self.EDGE_RATIO, self.MAX_XY - self.EDGE_RATIO,  self.SQUARE_RATIO + self.EDGE_RATIO):
                cv.line(img, (i, 0), (i, self.MAX_XY), (0, 255, 0), 1)
                cv.line(img, (i + self.SQUARE_RATIO, 0), (i + self.SQUARE_RATIO, self.MAX_XY), (0, 255, 0), 1)

                cv.line(img, (0, i), (self.MAX_XY, i), (0, 255, 0), 1)
                cv.line(img, (0, i + self.SQUARE_RATIO), (self.MAX_XY, i + self.SQUARE_RATIO), (0, 255, 0), 1)

        #cv.imshow('grid', img)
        #cv.waitKey(0)
        #cv.destroyAllWindows()



#### helper functions ####
        
def contour_is_circular(contour: MatLike):
    """
    ### Contour is circular
    ---------------
    Function that checks if a contour is circular.
    
    #### Args:
    * contour: Contour of the object in the image.
    """

    # Approximate the contour
    perimeter = cv.arcLength(contour, True)
    area = cv.contourArea(contour)
    circularity = 4 * np.pi * (area / (perimeter ** 2))

    # Check the circularity
    check_1 = False
    if 0.6 < circularity < 1.4:
        # This contour is close to a circle
        check_1 = True

    # Fit a bounding rectangle and check the aspect ratio
    x, y, w, h = cv.boundingRect(contour)
    aspect_ratio = float(w) / h
    check_2 = False
    if 0.6 < aspect_ratio < 1.4:
        # The contour is close to being contained in a square
        check_2 = True

    # Minimum enclosing circle
    (x, y), radius = cv.minEnclosingCircle(contour)
    circle_area = np.pi * (radius ** 2)
    check_3 = False
    if 0.6 < (area / circle_area) < 1.4:
        # The area of the contour is close to that of the enclosing circle
        check_3 = True
    
    if check_1 and check_2 and check_3:
        return True

    return False


# Euclidian Distance
def distance(p1:float, p2:float):
    """
    p1 = (x1,y1)
    p2 = (x2,y2)
    """
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Finds center point of contour 
def find_center_of_contour(contour: MatLike):   
    """
    Finds Center point of a single contour
    ---------
    contour: single contour

    """
    M = cv.moments(contour)  

    # avoiding division by zero
    if M["m00"] != 0:
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])
    
        return (x, y)
    else:
        
        return None

# Finds center point of points
def find_center_of_points(points: list[tuple]):
    """
    Finds Center point of a list of points
    ---------
    points: list of points

    """
    x = 0
    y = 0

    for point in points:
        x += point[0]
        y += point[1]

    return (x//len(points), y//len(points))

# Translates the x,y coordinates to the equivalent index of grid_ds.
def xy_to_index(Grid:Grid , x:int , y:int):
    """
    ### XY to index
    ---------------
    Function that translates the x,y coordinates to the equivalent index of grid_ds.
    
    #### Args:
    * x: x coordinate of the point
    * y: y coordinate of the point
    * Grid: Grid object

    #### Returns:
    * index of the point in the grid_ds
    """

    x_index = int(round(x // Grid.SQUARE_LENGTH))
    y_index = int(round(y // Grid.SQUARE_LENGTH))

    return (min(x_index, Grid.MAX_INDEX), min(y_index, Grid.MAX_INDEX))

# Same as above but taking into consideration the skewing that happens near the outter squares.
def xy_to_index_skewed(Grid: Grid, x: int, y: int, a:float):

    middle_index_tl_x = (Grid.SQUARE_LENGTH * Grid.MAX_INDEX)/2
    middle_index_tl_y = (Grid.SQUARE_LENGTH * Grid.MAX_INDEX)/2
    
    index_x, index_y = xy_to_index(Grid, x , y)

    offset_x = int(abs(middle_index_tl_x - index_x)**a)
    offset_y = int(abs(middle_index_tl_y - index_y)**a)

    index_x_skewed = int(round(x // (Grid.SQUARE_LENGTH + offset_x)))
    index_y_skewed = int(round(y // (Grid.SQUARE_LENGTH + offset_y)))

    return (min(index_x_skewed, Grid.MAX_INDEX), min(index_y_skewed, Grid.MAX_INDEX))

# Translates the index to the equivalent x,y coordinates of grid_ds top left point.   
def index_to_xy(Grid:Grid, x_index:int, y_index:int):
    """
    ### Index to XY
    ---------------
    Function that translates the index to the equivalent x,y coordinates of grid_ds tl point.

    #### Args:
    * x_index: x index of the point
    * y_index: y index of the point
    * grid_ds: Grid object

    #### Returns:
    * x,y coordinates of the top left point of the square
    """
   
    x = (x_index) * Grid.SQUARE_LENGTH
    y = (y_index) * Grid.SQUARE_LENGTH

    return (x, y) # top left point of square