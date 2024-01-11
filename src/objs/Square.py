from ast import Tuple
import cv2 as cv
import numpy as np

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
    def __init__(self, tl: int, br: int, index: Tuple, PIN_RATIO: int, PLUS_MINUS: int, img = None):
        #self.id = id
        
        self.p_pin_count = 0
        self.p_pins = []
        self.pins = []

        self.is_block = False
        self.block_type = ''

        # coordinates and index in Grid
        self.tl = tl; self.br = br
        self.index = index

        self.corners = self.add_corners(PIN_RATIO, PLUS_MINUS)
        self.img = img.copy()
        self.img_of_sq = self.createImg(img.copy()) # a cutout of the square from the image


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

    def createImg(self, img):
        return img[(self.tl[1]-10):(self.br[1]+10), (self.tl[0]-10):(self.br[0]+10)]

    def add_corners(self, PIN_RATIO, PLUS_MINUS, p=3, a = 1.5):

        tl_x, tl_y = self.tl
        br_x, br_y = self.br
        
        if self.index[0] != 4:
            SKEW_x = int((abs(self.index[0] - 4) ** a) * ((self.index[0] - 4)/ abs(self.index[0] - 4)))
        else:
            SKEW_x = 0
        
        if self.index[1] != 4:
            SKEW_y = int((abs(self.index[1] - 4) ** a) * ((self.index[1] - 4)/ abs(self.index[1] - 4)))
        else:
            SKEW_y = 0
        
        top_right = (
            (
                tl_x - (p*PLUS_MINUS) + SKEW_x, 
                tl_y - (p*PLUS_MINUS) + SKEW_y
            ),
            (
                tl_x + PIN_RATIO + (p*PLUS_MINUS) + SKEW_x, 
                tl_y + PIN_RATIO + (p*PLUS_MINUS) + SKEW_y
            )
        )

        top_left = (
            (
                br_x - PIN_RATIO - (p*PLUS_MINUS) + SKEW_x,
                tl_y - (p*PLUS_MINUS) + SKEW_y
            ),
            (
                br_x + (p*PLUS_MINUS) + SKEW_x,
                tl_y + PIN_RATIO + (p*PLUS_MINUS) + SKEW_y
            )
        )

        bottom_right = (
            (
                tl_x - (p*PLUS_MINUS) + SKEW_x, 
                br_y - PIN_RATIO - (p*PLUS_MINUS) + SKEW_y
            ),
            (
                tl_x + PIN_RATIO+(p*PLUS_MINUS) + SKEW_x, 
                br_y + (p*PLUS_MINUS) + SKEW_y
            )
        )

        bottom_left = (
            (
                br_x - PIN_RATIO - (p*PLUS_MINUS) + SKEW_x,
                br_y - PIN_RATIO - (p*PLUS_MINUS) + SKEW_y
            ),
            (
                br_x + (p*PLUS_MINUS) + SKEW_x, 
                br_y + (p*PLUS_MINUS) + SKEW_y
            )
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
    
    def which_corner_is_contour_in(self, contour):
        corn = ["top_right", "top_left", "bottom_right", "bottom_left" ]

        x, y = cv.boundingRect(contour)[:2]

        i = 0
        for corner in self.corners:
            if x >= corner[0][0] and x <= corner[1][0]:
                if y >= corner[0][1] and y <= corner[1][1]:
                    return corn[i]
            i += 1


        # might be unecessary after corner skewing
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



    def get_rgb_avg_of_contour(self, contour, corner='', print_flag = 1):
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

        mask = np.zeros(image.shape[:2], dtype=np.uint8)  # Create a mask with the same height and width as the image
        cv.drawContours(mask, [contour], 0, (255), -1)  # Fill the contour on the mask

        # Extract the pixels inside the contour
        pixels_inside = image[mask == 255]

        # Calculate the average RGB values
        average_rgb = np.mean(pixels_inside, axis=0)
        
        # Remove NaN values 
        average_rgb = np.nan_to_num(average_rgb)

        if print_flag:
            print(f"     {corner}: ", [round(x) for x in average_rgb ])

        return [round(x) for x in average_rgb ]

    def get_pins_rgb(self, pf=1):
        pins_rgb = []

        for pins in self.pins:
            corner = self.which_corner_is_contour_in(pins)
            pins_rgb.append(self.get_rgb_avg_of_contour(pins, corner, pf))

        return pins_rgb, corner  # tr, tl, br, bl corners 