import cv2 as cv

class Grid:
    """
    ### Grid
    ---------------
    Class that represents the grid

    #### Args:
    * img: scanned image of the grid

    #### Attributes:
    * img: scanned image of the grid 
    * MAX_XY: maximum x,y coordinate of the image (assumes image is square)
    * PIN_RATIO: ratio of the pin size 
    * EDGE_RATIO: ratio of the edge size 
    * SQUARE_RATIO: ratio of the square size 
    * PLUS_MINUS: tolerance for the pin size 
    * SQUARE_LENGTH: length of the square (SQUARE_RATIO + EDGE_RATIO)
    * MAX_INDEX: maximum index of the grid (9)
    * grid: "map" (list of lists) of squares in the grid.
    """
    def __init__(self, img):
        # scanned image
        self.img = img.copy()

        self.MAX_XY = self.img.shape[0] # assumes image is square

        # ratios measured experimentally 
        self.PIN_RATIO = round(self.MAX_XY * 0.012)
        self.EDGE_RATIO = round(self.MAX_XY * 0.012)
        self.SQUARE_RATIO = round(self.MAX_XY * 0.088)
        self.PLUS_MINUS = round(self.MAX_XY * 0.005)

        self.SQUARE_LENGTH = self.SQUARE_RATIO + (self.EDGE_RATIO)

        self.MAX_INDEX = 9  # assumes grid is square 

        
        self.grid = self.create_grid()

    # Translates the x,y coordinates to the equivalent index of grid_ds.
    def xy_to_index(self, x, y):
        """
        ### XY to index
        ---------------
        Function that translates the x,y coordinates of a pin to the equivalent index of grid_ds.
        
        #### Args:
        x: x coordinate of the pin
        y: y coordinate of the pin
        grid_ds: grid_ds:[ block_width, [[ square{tl, br, block} , ...], ...] ]

        #### Returns:
        Index of the pin in grid_ds
        """

        x_index = int(round(x // self.SQUARE_LENGTH))
        y_index = int(round(y // self.SQUARE_LENGTH))

        return (min(x_index, self.MAX_INDEX), min(y_index, self.MAX_INDEX))

    # Translates the index to the equivalent x,y coordinates of grid_ds tl point.   
    def index_to_xy(self, x_index, y_index):
        """
        ### Index to xy
        ---------------
        Function that translates the index of a pin to the equivalent x,y coordinates of grid_ds.
        
        #### Args:
        x_index: x index of the pin
        y_index: y index of the pin
        grid_ds: grid_ds:[ block_width, [[ square{tl, br, block} , ...], ...] ]

        #### Returns:
        x,y coordinates of the pin
        """
        x = (x_index) * self.SQUARE_LENGTH
        y = (y_index) * self.SQUARE_LENGTH

        return (x, y) # tl point
    
    # Appends squares to the grid map.
    def append(self, x_index, y_index, square):
        """ appends square to grid_ds"""
        
        if self.grid[x_index][y_index] != None:
           print('ERROR: Square already exists and is being replaced')
       
        self.grid[x_index][y_index] = square
    
    def create_grid(self):
        """
        ### Create grid
        ---------------
        Function that creates a "map" (list of lists) of squares in the grid.

        #### Args:
        * img: image to show the grid lines on
        
        #### Returns:
        * Grid object
        """

        # initialize grid_ds with None values  
        grid = [[None for _ in range(self.MAX_INDEX + 1)] for _ in range(self.MAX_INDEX + 1)]

        # stop values for the for loops
        STOP_XY = self.MAX_XY - self.EDGE_RATIO
        STEP = self.SQUARE_RATIO + self.EDGE_RATIO

        # create a "map" (list of lists) of squares in the grid
        for x in range(0, STOP_XY, STEP):
            for y in range(0, STOP_XY, STEP):
                
                x_index, y_index = self.xy_to_index(x, y)

                # create a square
                sq = Square(
                    (x + (self.EDGE_RATIO), y + (self.EDGE_RATIO)), 
                    (x + self.SQUARE_RATIO + (self.EDGE_RATIO), y + self.SQUARE_RATIO + (self.EDGE_RATIO)), 
                    (x_index, y_index)
                )
                
                # color the squares in a chessboard pattern
                '''
                if    (j%2 == 0 and i%2 == 0): color = (0, 0, 255)
                elif  (j%2 == 0 and i%2 == 1): color = (0, 255, 0)
                elif  (j%2 == 1 and i%2 == 0): color = (255, 255, 0)
                else: color = (255, 0, 0)
                cv.rectangle(scaned_image_copy, sq["tl"], sq["br"], color, 1)
                #'''

                # add the square to the grid_ds list            
                grid[x_index][y_index] = sq
                
                # show the grid squares on the image each step
                """
                cv.imshow('grid', scaned_image_copy)
                cv.waitKey(0)
                cv.destroyAllWindows()
                #"""

        return grid

    def find_blocks(self, contours):

        image_copy = self.img.copy()

        # counts the number of pins in each square
        for p_pin in contours:
            x, y, w, h = cv.boundingRect(p_pin)

            # checks if the contour is around the size of a pin. 
            if  h <= self.PIN_RATIO + self.PLUS_MINUS and w <= self.PIN_RATIO + self.PLUS_MINUS: 
                if h > self.PIN_RATIO - self.PLUS_MINUS and w > self.PIN_RATIO - self.PLUS_MINUS: 
                    cv.rectangle(image_copy, (x, y), (x+self.PIN_RATIO, y+self.PIN_RATIO), (0, 255, 0), 1)
                    x_index, y_index = self.xy_to_index(x, y) 

                    x_index = min(x_index, self.MAX_INDEX)
                    y_index = min(y_index, self.MAX_INDEX)
                    
                    self.grid[x_index][y_index].pin_count += 1

        # squares with n or more pins are considered blocks
        blocks_found = 0
        for x in self.grid:
            for y in x:
                if y.pin_count >= 2:
                    y.is_block = True
                    #print(f"block found at {self.xy_to_index(y.tl[0], y.tl[1])}")
                    cv.rectangle(image_copy, y.tl, y.br, (255, 0, 0), 1)
                    cv.rectangle(image_copy, (y.tl[0]-self.EDGE_RATIO, y.tl[1]-self.EDGE_RATIO), (y.br[0]+self.EDGE_RATIO, y.br[1]+self.EDGE_RATIO), (0, 255, 0), 1)
                    blocks_found += 1
        
        print(f"blocks found: {blocks_found}")
            
        '''
        cv.imshow('block', image_copy)
        cv.waitKey(0)
        cv.destroyAllWindows()
        #'''



    # Shows the grid lines on the image.
    def show_gridLines(self):
        """
        ### Show grid lines
        ---------------
        Function that shows the grid lines on the image.
        
        #### Args:
        * img: image to show the grid lines on
        * grid_ds: Grid object

        #### Returns:
        None
        """
        img = self.img.copy()
        for i in range(0 + self.EDGE_RATIO, self.MAX_XY - self.EDGE_RATIO,  self.SQUARE_RATIO + self.EDGE_RATIO):
            for j in range(0 + self.EDGE_RATIO, self.MAX_XY - self.EDGE_RATIO,  self.SQUARE_RATIO + self.EDGE_RATIO):
                cv.line(img, (i, 0), (i, self.MAX_XY), (0, 255, 0), 1)
                cv.line(img, (i + self.SQUARE_RATIO, 0), (i + self.SQUARE_RATIO, self.MAX_XY), (0, 255, 0), 1)

                cv.line(img, (0, i), (self.MAX_XY, i), (0, 255, 0), 1)
                cv.line(img, (0, i + self.SQUARE_RATIO), (self.MAX_XY, i + self.SQUARE_RATIO), (0, 255, 0), 1)

        cv.imshow('grid', img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    

class Square:
    """
    ### Square
    ---------------
    Class that represents a square in the grid_ds.
    
    #### Args:
    * tl: top left point of the square
    * br: bottom right point of the square
    * index: index of the square in the grid_ds
    
    #### Attributes:
    * tl: top left point of the square
    * br: bottom right point of the square
    * index: index of the square in the grid_ds
    * block: boolean that indicates if the square is a block
    * pin_count: number of pins in the square
    """
    def __init__(self, tl, br, index, id = None, img=None):
        
        # identification and cropped image
        #self.id = id
        #img = img
        self.is_Block = False
        self.contour_count = 0
        self.pin_count = 0

        # coordinates and index in Grid
        self.tl = tl; self.br = br
        self.index = index
        

        

