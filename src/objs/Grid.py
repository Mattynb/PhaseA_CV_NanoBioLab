import cv2 as cv
from cv2.typing import MatLike
from .Square import Square

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
                if sq.p_pin_count >= 3:
                    for p_pin in sq.p_pins:
                        x, y, w, h = cv.boundingRect(p_pin)
                        
                        # checks if top left or bottom right point of pin is inside corner of square
                        if sq.is_in_corners(x, y) or sq.is_in_corners(x+int(w), y+int(h)):
                            
                            sq.add_pin(p_pin)
                            sq.draw_pins(image_copy)
                            sq.draw_corners(image_copy)

                
                    
        # checks if the square has 2 or more pins and if it does, it is considered a block.
        blocks_found = 0
        for x in self.grid:
            for sq in x:
                if len(sq.pins) >= 2:
                    sq.is_block = True
                    blocks_found += 1

                    """
                    cv.imshow('block', sq.img)
                    cv.waitKey(0)
                    cv.destroyAllWindows()
                    #"""
                    
                    # outputs the rgb sequence of the pins in the block
                    #"""
                    print(f"Square at index: {sq.index}", "{", sq.get_pins_rgb(), "}\n") 
                    #"""


        # shows image with pins and corners drawn
        #'''
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


        # iterate through the contours.
        # if they are around the size of a pin, add them to the corresponding square in the grid.
        for p_pin in contours:
            x, y, w, h = cv.boundingRect(p_pin) 

            # checks if the contour is around the size of a pin and adds it to the square if it is
            if  h <= self.PIN_RATIO + (2*self.PLUS_MINUS) and w <= self.PIN_RATIO + (2*self.PLUS_MINUS): 
                if h > self.PIN_RATIO - (2*self.PLUS_MINUS) and w > self.PIN_RATIO - (2*self.PLUS_MINUS): 
                
                    x_index, y_index = xy_to_index(self, x, y)

                    x_index = min(x_index, self.MAX_INDEX)
                    y_index = min(y_index, self.MAX_INDEX)

                    self.grid[x_index][y_index].add_p_pin(p_pin)
                    self.grid[x_index][y_index].p_pin_count += 1
         
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
    def show_gridLines(self):
        """
        ### Show grid lines
        ---------------
        Function that shows the grid lines on the image.
        """
        
        img = self.img.copy()
        
        # draw grid lines
        for i in range(0 + self.EDGE_RATIO, self.MAX_XY - self.EDGE_RATIO,  self.SQUARE_RATIO + self.EDGE_RATIO):
            for j in range(0 + self.EDGE_RATIO, self.MAX_XY - self.EDGE_RATIO,  self.SQUARE_RATIO + self.EDGE_RATIO):
                cv.line(img, (i, 0), (i, self.MAX_XY), (0, 255, 0), 1)
                cv.line(img, (i + self.SQUARE_RATIO, 0), (i + self.SQUARE_RATIO, self.MAX_XY), (0, 255, 0), 1)

                cv.line(img, (0, i), (self.MAX_XY, i), (0, 255, 0), 1)
                cv.line(img, (0, i + self.SQUARE_RATIO), (self.MAX_XY, i + self.SQUARE_RATIO), (0, 255, 0), 1)

        cv.imshow('grid', img)
        cv.imwrite(r'C:\Users\Matheus\Desktop\NanoTechnologies_Lab\Phase A\src\Image\demo_imgs\grid.jpg', img)
        cv.waitKey(0)
        cv.destroyAllWindows()



#### helper functions ####
        
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

# Translates the index to the equivalent x,y coordinates of grid_ds tl point.   
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