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

    
    """
    cv.imshow('img_hsv', img_hsv)
    cv.imshow('mask', color_mask)
    cv.waitKey(0)
    cv.destroyAllWindows()
    #"""
   

    # Apply the mask to the original image using bitwise_and
    result = cv.bitwise_and(scaned_image_copy, scaned_image_copy, mask=color_mask)
    
    draw_recognized(result, scaned_image_copy)


def draw_recognized(result, scaned_image):
    edges = cv.Canny(result, 100, 200)
    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    
       
    xx = scaned_image.shape[0]
    yy = scaned_image.shape[1] 
    pin_ratio = round(scaned_image.shape[1] * 0.01)
    edge_ratio = round(scaned_image.shape[1] * 0.01)
    plus_minus = round(scaned_image.shape[1] * 0.005)

    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)

        # checks if the contour is inside edges of the grid and if its around the size of a pin.
        if x > edge_ratio and y > edge_ratio: 
            if x+w < xx - edge_ratio and y+h < yy - edge_ratio:
                if  h <= pin_ratio + plus_minus and w <= pin_ratio + plus_minus: 
                    if h > pin_ratio - plus_minus and w > pin_ratio - plus_minus: 
                        cv.rectangle(scaned_image, (x, y), (x+w, y+h), (0, 255, 0), 1)

    cv.imshow('contour', scaned_image)

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

