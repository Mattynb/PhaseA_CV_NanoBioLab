import cv2 as cv
import numpy as np

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
    
    # Creates a "map" (list of lists) of squares in the grid.
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
                    (x_index, y_index),
                    self.PIN_RATIO,
                    self.PLUS_MINUS,
                    self.img
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

        # the potential pins (p_pins) and adds them to the appropriate squares
        self.find_p_pins(contours)

        # checks if the pin is in the corners of the square and adds it to the square if it is
        for x in self.grid:
            for sq in x:
                if sq.p_pin_count >= 2:
                    for p_pin in sq.p_pins:
                        x, y, w, h = cv.boundingRect(p_pin)
                        
                        if sq.is_in_corners(x, y) or sq.is_in_corners(x+int(w), y+int(h)):
                            
                            sq.add_pin(p_pin)
                            sq.draw_pins(image_copy)
                            sq.draw_corners(image_copy)

                    c,r = sq.index
                    print("Square at index: ", (r,c) , "{")
                    sq.get_pins_rgb()
                    print("}")
                            
        blocks_found = 0
        for x in self.grid:
            for sq in x:
                if len(sq.pins) >= 2:
                    sq.is_block = True
                    blocks_found += 1

        #'''
        cv.imshow('blocks', image_copy)
        cv.waitKey(0)
        cv.destroyAllWindows()
        #'''



    def get_rgb_avg_of_area(self, x, y, w, h):
        """ 
        ### Get RGB average of area
        ---------------
        Function that gets the average RGB of an area of the image.
        
        #### Args:
        * x: x coordinate of the top left point of the area
        * y: y coordinate of the top left point of the area
        * w: width of the area
        * h: height of the area
        
        #### Returns:
        * Average RGB of the area
        """
        
        # crop the image
        image_copy = self.img.copy()
        crop = image_copy[y:y+h, x:x+w]

        # get the average of each channel
        avg_color_per_row = np.average(crop, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        avg_color = np.uint8(avg_color)

        return avg_color        

    def find_p_pins(self, contours):

        for p_pin in contours:
            x, y, w, h = cv.boundingRect(p_pin) 
            # checks if the contour is around the size of a pin and adds it to the square if it is
            if  h <= self.PIN_RATIO + (2*self.PLUS_MINUS) and w <= self.PIN_RATIO + (2*self.PLUS_MINUS): 
                if h > self.PIN_RATIO - (2*self.PLUS_MINUS) and w > self.PIN_RATIO - (2*self.PLUS_MINUS): 
                
                    x_index, y_index = self.xy_to_index(x, y)

                    x_index = min(x_index, self.MAX_INDEX)
                    y_index = min(y_index, self.MAX_INDEX)

                    self.grid[x_index][y_index].add_p_pin(p_pin)
                    self.grid[x_index][y_index].p_pin_count += 1

    


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
        cv.imwrite(r'C:\Users\Matheus\Desktop\NanoTechnologies_Lab\Phase A\src\Image\demo_imgs\grid.jpg', img)
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
    def __init__(self, tl, br, index, PIN_RATIO, PLUS_MINUS, img=None):
        
        # identification and cropped image
        #self.id = id
        self.img = img
        self.is_Block = False
        self.contour_count = 0
        self.p_pin_count = 0
        self.p_pins = []
        self.pins = []

        # coordinates and index in Grid
        self.tl = tl; self.br = br
        self.index = index

        self.corners = self.add_corners(PIN_RATIO, PLUS_MINUS)
    

    def add_p_pin(self, p_pin):
        self.p_pins.append(p_pin)
       
    def add_pin(self, pin):
        self.pins.append(pin)
        
    def draw_pins(self, image):
        for pin in self.pins:
            cv.drawContours(image, pin, -1, (0, 255, 0), 1)      
    
    def draw_corners(self, img):
        for corner in self.corners:
            cv.rectangle(img, corner[0], corner[1], (0, 0, 255), 1)


    def add_corners(self, PIN_RATIO, PLUS_MINUS):
        top_right = (
            (self.tl[0]-(2*PLUS_MINUS), self.tl[1]-(2*PLUS_MINUS)),
            (self.tl[0]+PIN_RATIO+(2*PLUS_MINUS), self.tl[1]+PIN_RATIO+(2*PLUS_MINUS))
        )

        top_left = (
            (self.br[0]-PIN_RATIO-(2*PLUS_MINUS), self.tl[1]-(2*PLUS_MINUS)),
            (self.br[0]+(2*PLUS_MINUS), self.tl[1]+PIN_RATIO+(2*PLUS_MINUS)),
        )

        bottom_right = (
            (self.tl[0]-(2*PLUS_MINUS), self.br[1]-PIN_RATIO-(2*PLUS_MINUS)),
            (self.tl[0]+PIN_RATIO+(2*PLUS_MINUS), self.br[1]+(2*PLUS_MINUS)),
        )

        bottom_left = (
            (self.br[0]-PIN_RATIO-(2*PLUS_MINUS), self.br[1]-PIN_RATIO-(2*PLUS_MINUS)),
            (self.br[0]+(2*PLUS_MINUS), self.br[1]+(2*PLUS_MINUS)),
        )

        return [top_left, top_right, bottom_left, bottom_right]

    def is_in_corners(self, x, y):
        #corn = ["top_left", "top_right", "bottom_left", "bottom_right"]

        i = 0
        for corner in self.corners:
            if x >= corner[0][0] and x <= corner[1][0]:
                if y >= corner[0][1] and y <= corner[1][1]:
                    #print(corn[i], ": ", round(self.get_rgb_avg_of_contour(contour)))
                    return True
            i += 1

        return False
    
    def what_corner_is_contour(self, contour):
        corn = ["top_right", "top_left", "bottom_right", "bottom_left" ]

        x, y = cv.boundingRect(contour)[:2]

        i = 0
        for corner in self.corners:
            if x >= corner[0][0] and x <= corner[1][0]:
                if y >= corner[0][1] and y <= corner[1][1]:
                    return corn[i]
            i += 1

        i =0
        for corner in self.corners:
            if x + 5 >= corner[0][0] and x + 5 <= corner[1][0]:
                if y+ 5  >= corner[0][1] and y+ 5  <= corner[1][1]:
                    return corn[i]
            i += 1
        
        i =0
        for corner in self.corners:
            if x-5 >= corner[0][0] and x-5 <= corner[1][0]:
                if y-5  >= corner[0][1] and y-5 <= corner[1][1]:
                    return corn[i]
            i += 1



    def get_rgb_avg_of_contour(self, contour, corner=''):
        """
        ### Get RGB average of contour
        ---------------
        Function that gets the average RGB of a contour in the image.
        
        #### Args:
        * contour: Contour of the object in the image.
        
        #### Returns:
        * avg_color: Average RGB color of the contour.
        """

        # crop the image
        image_copy = self.img.copy()
        
        image = cv.cvtColor(image_copy, cv.COLOR_BGR2RGB)  # Convert to RGB format

        # Assuming 'contour' is your contour and 'image' is your image
        mask = np.zeros(image.shape[:2], dtype=np.uint8)  # Create a mask with the same height and width as the image
        cv.drawContours(mask, [contour], 0, (255), -1)  # Fill the contour on the mask

        # Extract the pixels inside the contour
        pixels_inside = image[mask == 255]

        # Calculate the average RGB values
        average_rgb = np.mean(pixels_inside, axis=0)

        print(f"     {corner}: ", [ round(x) for x in average_rgb ])

    def get_pins_rgb(self):
        pins_rgb = []

        for pins in self.pins:
            corner = self.what_corner_is_contour(pins)
            pins_rgb.append(self.get_rgb_avg_of_contour(pins, corner))

        return pins_rgb  # tl, tr, bl, br corners 