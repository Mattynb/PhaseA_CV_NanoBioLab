import numpy as np
import cv2 as cv

"""
global MAX_X
global MAX_Y
global PIN_RATIO 
global EDGE_RATIO
global BLOCK_RATIO 
global PLUS_MINUS
"""

# A function that pre-processes the image to isolate the color of the pins.
def pre_process(scaned_image):

    scaned_image_copy = scaned_image.copy()

    # Convert the image to HSV color space
    img_hsv = cv.cvtColor(scaned_image_copy, cv.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the color you want to isolate
    lower_color = np.array([0, 50, 0])
    upper_color = np.array([255, 255, 255])

    """kernel = np.ones((9,9), np.uint8)
    img_hsv = cv2.morphologyEx(img_hsv, cv2.MORPH_CLOSE, kernel, iterations=2)
    """
    # Create a mask using the inRange function
    color_mask = cv.inRange(img_hsv, lower_color, upper_color)

    # blur the mask to help remove noise, then apply the mask to the frame 
    #color_mask = cv.medianBlur(color_mask, 5)
 
    """
    cv.imshow('img_hsv', img_hsv)
    cv.imshow('mask', color_mask)
    cv.waitKey(0)
    cv.destroyAllWindows()
    #"""
   
    # Apply the mask to the original image using bitwise_and
    result = cv.bitwise_and(scaned_image_copy, scaned_image_copy, mask=color_mask)
    
    '''
    draw_recognized(result, scaned_image_copy)
    cv.waitKey(0)
    cv.destroyAllWindows()
    #'''
    
    edges = cv.Canny(color_mask, 0, 255)
    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    cv.imshow('edge', edges)
    cv.imshow('mask', color_mask)
    cv.waitKey(0)
    cv.destroyAllWindows()

    return contours

def draw_recognized(result, scaned_image) -> list:
    """
    ### Draw recognized
    ---------------
    Function that draws a rectangle around the recognized pins.
    
    #### Args:
    result: image where contours are found
    scaned_image: image where the rectangles are drawn
    
    #### Returns:
    List of contours
    """

    edges = cv.Canny(result, 100, 200)
    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    
    MAX_X = scaned_image.shape[0]
    MAX_Y = scaned_image.shape[1] 
    PIN_RATIO = round(scaned_image.shape[1] * 0.01)
    EDGE_RATIO = round(scaned_image.shape[1] * 0.01)
    PLUS_MINUS = PIN_RATIO#round(scaned_image.shape[1] * 0.005)

    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)

        # checks if the contour is inside edges of the grid and if its around the size of a pin.
        if x > EDGE_RATIO and y > EDGE_RATIO: 
            if x+w < MAX_X - EDGE_RATIO and y+h < MAX_Y - EDGE_RATIO:
                if  h <= PIN_RATIO + PLUS_MINUS and w <= PIN_RATIO + PLUS_MINUS: 
                    if h > PIN_RATIO - PLUS_MINUS and w > PIN_RATIO - PLUS_MINUS: 
                        cv.rectangle(scaned_image, (x, y), (x+PIN_RATIO, y+PIN_RATIO), (0, 255, 0), 1)

    cv.imshow('contour', scaned_image)
   

    return contours

def grid(scaned_image):
    """
    ### Grid
    ---------------
    Function that draws a grid on the image.
    """
    
    scaned_image_copy = scaned_image.copy()
    
    global MAX_X
    global MAX_Y
    global PIN_RATIO 
    global EDGE_RATIO
    global BLOCK_RATIO 
    global PLUS_MINUS

    MAX_X = scaned_image_copy.shape[0]
    MAX_Y = scaned_image_copy.shape[1]
    PIN_RATIO = round(scaned_image_copy.shape[1] * 0.012)
    PLUS_MINUS = round(scaned_image_copy.shape[1] * 0.005)
    EDGE_RATIO = round(scaned_image_copy.shape[1] * 0.0109)
    BLOCK_RATIO = round(scaned_image_copy.shape[1] * 0.088)

    grid_ds = [BLOCK_RATIO + (EDGE_RATIO)]
    square = {"tl": 0, "br": 0, "block": False, "pin_count": 0} # [[{top left:(x,y), bottom right:(MAX_X, MAX_Y), is_block: True}]

    for i in range(0, MAX_X - EDGE_RATIO, BLOCK_RATIO + EDGE_RATIO):
        for j in range(0, MAX_Y - EDGE_RATIO, BLOCK_RATIO + EDGE_RATIO):

            # create a square
            sq = square.copy()
            sq["tl"] = (i, j)
            sq["br"] = (i + BLOCK_RATIO + (2*EDGE_RATIO), j + BLOCK_RATIO + (2*EDGE_RATIO))
     
            # color the blocks in a chessboard pattern
            '''
            if    (j%2 == 0 and i%2 == 0): color = (0, 0, 255)
            elif  (j%2 == 0 and i%2 == 1): color = (0, 255, 0)
            elif  (j%2 == 1 and i%2 == 0): color = (255, 255, 0)
            else: color = (255, 0, 0)
            cv.rectangle(scaned_image_copy, sq["tl"], sq["br"], color, 1)
            #'''

            # add the square to the grid_ds list
            x_index, y_index = xy_to_index(i, j, grid_ds)
            if x_index == 0 and y_index == 0:
                grid_ds.append([[sq]])
            elif y_index == 0:
                grid_ds[1].append([sq])
            else:
                grid_ds[1][x_index].append(sq)
            
            # show the grid squares on the image each step
            """
            cv.imshow('grid', scaned_image_copy)
            cv.waitKey(0)
            cv.destroyAllWindows()
            grid_ds.append(sq)
            #"""
    
    # show the grid lines on the image
    """
    for i in range(0 + EDGE_RATIO, MAX_X - EDGE_RATIO,  BLOCK_RATIO + EDGE_RATIO):
        for j in range(0 + EDGE_RATIO, MAX_Y - EDGE_RATIO,  BLOCK_RATIO + EDGE_RATIO):
            cv.line(scaned_image_copy, (i, 0), (i, MAX_X), (0, 255, 0), 1)
            cv.line(scaned_image_copy, (i + BLOCK_RATIO, 0), (i + BLOCK_RATIO, MAX_X), (0, 255, 0), 1)

            cv.line(scaned_image_copy, (0, i), (MAX_Y, i), (0, 255, 0), 1)
            cv.line(scaned_image_copy, (0, i + BLOCK_RATIO), (MAX_Y, i + BLOCK_RATIO), (0, 255, 0), 1)
    #"""

    # show the grid square on the image final step
    """
    cv.imshow('grid', scaned_image_copy)
    cv.waitKey(0)
    cv.destroyAllWindows()
    grid_ds.append(sq)
    #"""

    #print(f"{len(grid_ds[1])} x {len(grid_ds[1][0])} ")

    return grid_ds

# A function that translates the x,y coordinates of a pin to the equivalent index of grid_ds.
def xy_to_index(x, y, grid_ds):
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
    
    x_index = int(round(x / grid_ds[0]))
    y_index = int(round(y / grid_ds[0]))

    return (x_index, y_index)

# A function that translates the index of a pin to the equivalent x,y coordinates of grid_ds.   
def index_to_xy(x_index, y_index, grid_ds):
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
    x = x_index * grid_ds[0]
    y = y_index * grid_ds[0]

    return (x, y)


def find_block(grid_ds, contours, scaned_image):
    """
    ### Find block
    ---------------
    Function that finds the position of every block that contains 4 pins.
    
    #### Args:
    grid_ds: grid_ds:[ block_width, [[ square{tl, br, block} , ...], ...] ]
    contours: list of contours

    #### Returns:
    Index of the block in grid_ds
    """
    scaned_image_copy = scaned_image.copy()

    print(f"len(contours): {len(contours)}")

    # each contour is a potential pin
    for p_pin in contours:
        x, y, w, h = cv.boundingRect(p_pin)

        '''if w > (PIN_RATIO + PLUS_MINUS) or w < (PIN_RATIO - PLUS_MINUS):
            #print(f"({w}), {PIN_RATIO})")
            continue
        if h > (PIN_RATIO + PLUS_MINUS) or h < (PIN_RATIO - PLUS_MINUS):
            #print(f"({y - h}, {PIN_RATIO})")
            continue'''
        
        x_index, y_index = xy_to_index(x, y, grid_ds)
        grid_ds[1][x_index][y_index]["pin_count"] += 1

    for x in grid_ds[1]:
        for y in x:
            if y["pin_count"] >= 3:
                y["block"] = True
                print(f"block found at {xy_to_index(y['tl'][0], y['tl'][1], grid_ds)}")
                cv.rectangle(scaned_image_copy, y["tl"], y["br"], (0, 0, 255), 1)

    cv.imshow('block', scaned_image_copy)
    cv.waitKey(0)
    cv.destroyAllWindows()

    return None








# function for testing parameters 
def adaptive_pre_process(scaned_image):
    """
    ### Adaptive pre-process
    ---------------
    Function that allows the user to select the color to be isolated by using trackbars.
    The function also draws a rectangle around the recognized pins.
    """
    scaned_image_copy = scaned_image.copy()

    # Convert the image to HSV color space
    img_hsv = cv.cvtColor(scaned_image_copy, cv.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the color you want to isolate
    lower_color = np.array([0, 50, 30])
    upper_color = np.array([255, 255, 255])

    buffer = lower_color.copy()
    while True:
        # Create a mask using the inRange function
        color_mask = cv.inRange(img_hsv, lower_color, upper_color)

        # Blur the mask to help remove noise, then apply the mask to the frame 
        color_mask = cv.medianBlur(color_mask, 5)

        # Apply the mask to the original image using bitwise_and
        result = cv.bitwise_and(scaned_image_copy, scaned_image_copy, mask=color_mask)
        
        cv.imshow('mask', color_mask)
        key = cv.waitKey(1) & 0xFF

        # Press 'q' to break the loop
        if key == ord('q'):
            break
        # Press 'h', 's', or 'v' to increment the respective lower_color value (0-255)
        elif key == ord('h'):
            lower_color[0] = max(min(lower_color[0]-1, 255), 0)
        elif key == ord('s'):
            lower_color[1] = max(min(lower_color[1]-1, 255), 0)
        elif key == ord('v'):
            lower_color[2] = max(min(lower_color[2]-1, 255), 0)
        elif key == ord('H'):
            lower_color[0] = max(min(lower_color[0]+1, 255), 0)
        elif key == ord('S'):
            lower_color[1] = max(min(lower_color[1]+1, 255), 0)
        elif key == ord('V'):
            lower_color[2] = max(min(lower_color[2]+1, 255), 0)

        
        if buffer[0] != lower_color[0] or buffer[1] != lower_color[1] or buffer[2] != lower_color[2]:
            print(lower_color)
            
            buffer = lower_color.copy()
            cv.destroyAllWindows()
            
            drawed = scaned_image_copy.copy()  
            draw_recognized(result, drawed)
   
    cv.destroyAllWindows()