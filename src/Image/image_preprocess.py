from tkinter import X
import cv2 as cv
import numpy as np

def pre_process(scaned_image):

    scaned_image_copy = scaned_image.copy()

    # Convert the image to HSV color space
    img_hsv = cv.cvtColor(scaned_image_copy, cv.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the color you want to isolate
    lower_color = np.array([0, 50, 30])
    upper_color = np.array([255, 255, 255])

    """kernel = np.ones((9,9), np.uint8)
    img_hsv = cv2.morphologyEx(img_hsv, cv2.MORPH_CLOSE, kernel, iterations=2)
    """
    # Create a mask using the inRange function
    color_mask = cv.inRange(img_hsv, lower_color, upper_color)

    # blur the mask to help remove noise, then apply the mask to the frame 
    color_mask = cv.medianBlur(color_mask, 5)

    
    #"""
    cv.imshow('img_hsv', img_hsv)
    cv.imshow('mask', color_mask)
    cv.waitKey(0)
    cv.destroyAllWindows()
    #"""
   

    # Apply the mask to the original image using bitwise_and
    result = cv.bitwise_and(scaned_image_copy, scaned_image_copy, mask=color_mask)
    
    draw_recognized(result, scaned_image_copy)
    cv.waitKey(0)
    cv.destroyAllWindows()

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
    
       
    xx = scaned_image.shape[0]
    yy = scaned_image.shape[1] 
    pin_ratio = round(scaned_image.shape[1] * 0.01)
    edge_ratio = round(scaned_image.shape[1] * 0.01)
    plus_minus = pin_ratio#round(scaned_image.shape[1] * 0.005)

    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)

        # checks if the contour is inside edges of the grid and if its around the size of a pin.
        if x > edge_ratio and y > edge_ratio: 
            if x+w < xx - edge_ratio and y+h < yy - edge_ratio:
                if  h <= pin_ratio + plus_minus and w <= pin_ratio + plus_minus: 
                    if h > pin_ratio - plus_minus and w > pin_ratio - plus_minus: 
                        cv.rectangle(scaned_image, (x, y), (x+pin_ratio, y+pin_ratio), (0, 255, 0), 1)

    cv.imshow('contour', scaned_image)
   

    return contours

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

def grid(scaned_image):
    """
    ### Grid
    ---------------
    Function that draws a grid on the image.
    """
    scaned_image_copy = scaned_image.copy()

    xx = scaned_image.shape[0]
    yy = scaned_image.shape[1] 
    pin_ratio = round(scaned_image.shape[1] * 0.01)
    edge_ratio = round(scaned_image.shape[1] * 0.0109)
    block_ratio = round(scaned_image.shape[1] * 0.088)
    plus_minus = round(scaned_image.shape[1] * 0.002)

    grid_ds = [block_ratio + (edge_ratio)]
    square = {"tl": 0, "br": 0, "block": False} # [[{top left:(x,y), bottom right:(xx, yy), is_block: True}]

    for i in range(0, xx - edge_ratio, block_ratio + edge_ratio):
        for j in range(0, yy - edge_ratio, block_ratio + edge_ratio):
    
            sq = square.copy()
            sq["tl"] = (i, j)
            sq["br"] = (i + block_ratio + (2*edge_ratio), j + block_ratio + (2*edge_ratio))
     
            if    j%2 == 0 and i%2 == 0: color = (0, 0, 255)
            elif  j%2 == 0 and i%2 == 1: color = (0, 255, 0)
            elif  j%2 == 1 and i%2 == 0: color = (255, 255, 0)
            else: color = (255, 0, 0)

            cv.rectangle(scaned_image_copy, sq["tl"], sq["br"], color, 1)
        
            x_index, y_index = xy_to_index(i, j, grid_ds)
            if x_index == 0 and y_index == 0:
                grid_ds.append([[sq]])
            elif y_index == 0:
                grid_ds[1].append([sq])
            else:
                grid_ds[1][x_index].append(sq)
            
            """
            cv.imshow('grid', scaned_image_copy)
            cv.waitKey(0)
            cv.destroyAllWindows()
            grid_ds.append(sq)
            #"""
    
    """
    for i in range(0 + edge_ratio, xx - edge_ratio,  block_ratio + edge_ratio):
        for j in range(0 + edge_ratio, yy - edge_ratio,  block_ratio + edge_ratio):
            cv.line(scaned_image_copy, (i, 0), (i, xx), (0, 255, 0), 1)
            cv.line(scaned_image_copy, (i + block_ratio, 0), (i + block_ratio, xx), (0, 255, 0), 1)

            cv.line(scaned_image_copy, (0, i), (yy, i), (0, 255, 0), 1)
            cv.line(scaned_image_copy, (0, i + block_ratio), (yy, i + block_ratio), (0, 255, 0), 1)
    #"""

    #"""
    cv.imshow('grid', scaned_image_copy)
    cv.waitKey(0)
    cv.destroyAllWindows()
    grid_ds.append(sq)
    #"""

    print(f"{len(grid_ds[1])} x {len(grid_ds[1][0])} ")


# create a function that translates the x,y coordinates of a pin to the equivalent index of grid_ds.
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
   
