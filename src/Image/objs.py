import cv2 as cv

class Grid:
    def __init__(self, img):
        # scanned image
        self.img = img.copy()

        self.MAX_X = self.img.shape[0] 
        self.MAX_Y = self.img.shape[1] 

        self.PIN_RATIO = round(self.MAX_X * 0.012)
        self.EDGE_RATIO = round(self.MAX_X * 0.012)
        self.SQUARE_RATIO = round(self.MAX_X * 0.088)
        self.PLUS_MINUS = round(self.MAX_X * 0.005)

        self.SQUARE_LENGTH = self.SQUARE_RATIO + (self.EDGE_RATIO)

        self.MAX_X_INDEX = 9
        self.MAX_Y_INDEX = 9

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

        #print(x_index, y_index, grid_ds[0], x, y)

        return (min(x_index, self.MAX_X_INDEX), min(y_index, self.MAX_Y_INDEX))

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

        #print(x, y, grid_ds[0], x_index, y_index)

        return (x, y) # tl point
    
    # Appends squares to the grid map.
    def append(self, x_index, y_index, square):
        #if self.grid[x_index][y_index] != None:
           #print('ERROR: Square already exists and is being replaced')
       
        self.grid[x_index][y_index] = square
    
    def create_grid(self):  
        grid = [[None for _ in range(self.MAX_X_INDEX + 1)] for _ in range(self.MAX_Y_INDEX + 1)]

        STOP_X = self.MAX_X - self.EDGE_RATIO
        STOP_Y = self.MAX_Y - self.EDGE_RATIO
        STEP = self.SQUARE_RATIO + self.EDGE_RATIO

        # create a list of squares in the grid
        for x in range(0, STOP_X, STEP):
            for y in range(0, STOP_Y, STEP):

                x_index, y_index = self.xy_to_index(x, y)#;print(x_index, y_index)

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

    def find_block(self, contours):
        for p_pin in contours:
            x, y, w, h = cv.boundingRect(p_pin)

            '''
            if w > (PIN_RATIO + PLUS_MINUS) or w < (PIN_RATIO - PLUS_MINUS):
                #print(f"({w}), {PIN_RATIO})")
                continue
            if h > (PIN_RATIO + PLUS_MINUS) or h < (PIN_RATIO - PLUS_MINUS):
                #print(f"({y - h}, {PIN_RATIO})")
                continue#'''
            
            #print("255", x, y, Grid_DS[0], scaned_image_copy.shape[0], scaned_image_copy.shape[1])
            
            x_index, y_index = self.xy_to_index(x, y) #; print( len(Grid_DS[1][0]),  len(Grid_DS[1][0][0]))

            x_index = min(x_index, self.MAX_X_INDEX)
            y_index = min(y_index, self.MAX_Y_INDEX)

            self.grid[x_index][y_index].pin_count += 1

        image_copy = self.img.copy()

        for x in self.grid:
            for y in x:
                if y.pin_count >= 3:
                    y.is_block = True
                    print(f"block found at {self.xy_to_index(y.tl[0], y.tl[1])}")
                    cv.rectangle(image_copy, y.tl, y.br, (255, 0, 0), 1)
                    cv.rectangle(image_copy, (y.tl[0]-self.EDGE_RATIO, y.tl[1]-self.EDGE_RATIO), (y.br[0]+self.EDGE_RATIO, y.br[1]+self.EDGE_RATIO), (0, 255, 0), 1)

        cv.imshow('block', image_copy)
        cv.waitKey(0)
        cv.destroyAllWindows()



    # Shows the grid lines on the image.
    def show_gridLines(self):
        img = self.img.copy()
        for i in range(0 + self.EDGE_RATIO, self.MAX_X - self.EDGE_RATIO,  self.SQUARE_RATIO + self.EDGE_RATIO):
            for j in range(0 + self.EDGE_RATIO, self.MAX_Y - self.EDGE_RATIO,  self.SQUARE_RATIO + self.EDGE_RATIO):
                cv.line(img, (i, 0), (i, self.MAX_X), (0, 255, 0), 1)
                cv.line(img, (i + self.SQUARE_RATIO, 0), (i + self.SQUARE_RATIO, self.MAX_X), (0, 255, 0), 1)

                cv.line(img, (0, i), (self.MAX_Y, i), (0, 255, 0), 1)
                cv.line(img, (0, i + self.SQUARE_RATIO), (self.MAX_Y, i + self.SQUARE_RATIO), (0, 255, 0), 1)

        cv.imshow('grid', img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    

class Square:
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
        

        

