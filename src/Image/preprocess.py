import numpy as np
import cv2 as cv

# A function that pre-processes the image to isolate the color of the pins.
def pre_process(scaned_image):
    """
    ### Pre-process
    ---------------
    Function that isolates the color of the pins.

    #### Args:
    scaned_image: image to be pre-processed

    #### Returns:
    List of contours
    """

    scaned_image_copy = scaned_image.copy()
    
    # Define the lower and upper bounds for the color you want to isolate
    """
    # Hue   Light   Saturation
    img_hls = cv.cvtColor(scaned_image_copy, cv.COLOR_BGR2HLS)
    lower_color = np.array([0, 0, 55])
    upper_color = np.array([179, 255, 255])
    hls_color_mask = cv.inRange(img_hls, lower_color, upper_color)
    #"""
    
    # Hue   Saturation  Value 
    img_hsv = cv.cvtColor(scaned_image_copy, cv.COLOR_BGR2HSV)
    hsv_lower_color = np.array([0, 55, 0])
    hsv_upper_color = np.array([180, 255, 255])
    color_mask = cv.inRange(img_hsv, hsv_lower_color, hsv_upper_color)
    
    #color_mask = cv.bitwise_and(hsv_color_mask, hls_color_mask)

    """
    cv.imshow('img_hsv', img_hsv)
    #cv.imshow('img_hls', img_hls)
    #cv.imshow('hsv_color_mask', hsv_color_mask)
    #cv.imshow('hls_color_mask', hls_color_mask)
    cv.imshow('color_mask', color_mask)
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

    """
    cv.imshow('result', result)
    cv.waitKey(0)
    cv.destroyAllWindows()#"""

    return contours


# A function that draws a rectangle around the recognized pins. Not being used right now. Instead using Grid.find_blocks() from src/objs.py
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

# A function for testing parameters. Not being used right now. 
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