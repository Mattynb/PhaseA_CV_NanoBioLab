import numpy as np
import cv2 as cv
from cv2.typing import MatLike


def _pre_process(scaned_image:MatLike):
    # Convert to grayscale
    gray = cv.cvtColor(scaned_image, cv.COLOR_BGR2GRAY)

    # Blur the image to reduce noise
    gray_blurred = cv.medianBlur(gray, 5)

    # Apply Hough Circle Transform
    circles = cv.HoughCircles(gray_blurred, cv.HOUGH_GRADIENT, 1, 20,
                            param1=30, param2=50, minRadius=0, maxRadius=0)

    # Ensure at least some circles were found
    if circles is not None:
        # Convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        # Loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # Draw the circle in the output image
            cv.circle(scaned_image, (x, y), r, (0, 255, 0), 4)

    # Display the result
    cv.imshow('Detected Circles', scaned_image)
    cv.waitKey(0)
    cv.destroyAllWindows()

    


# A function that pre-processes the image to isolate the color of the pins.
def pre_process(scaned_image:MatLike):
    """
    ### Pre-process
    ---------------
    Function that pre-processes the image to isolate the color of the pins.

    #### Args:
    scaned_image: image to be pre-processed

    #### Returns:
    List of contours
    """

    scaned_image_copy = scaned_image.copy()
    
    # Convert the image to HSV color space. Hue Saturation Value.
    img_hsv = cv.cvtColor(scaned_image_copy, cv.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the color you want to isolate
    hsv_lower_color = np.array([0, 55, 0])
    hsv_upper_color = np.array([180, 255, 255])

    # Create a mask to filter out the grayscale colors isolating the color of the pins.
    color_mask = cv.inRange(img_hsv, hsv_lower_color, hsv_upper_color)
    edges = cv.Canny(color_mask, 0, 255)

    # Find the contours around the edges of the color mask.
    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    # Show the result of the pre-processing.
    #"""
    edges = cv.resize(edges, (500,500))
    cv.imshow('result', edges) #color_mask)
    cv.waitKey(250)
    cv.destroyAllWindows()
    #"""

    scaned_image = white_balance(scaned_image)

    return contours



"""
TODO: Add a descriptive pre_precess function that shows all the steps using the currently commented code in the pre_process function.
"""

def white_balance(image):

        reference_size=(20, 20)
        reference_top_left=(62, 80)

        

        # Create the reference 10x10 square for the reference region for white balancing
        reference_region = image[reference_top_left[1]:reference_top_left[1] + reference_size[1],
                                reference_top_left[0]:reference_top_left[0] + reference_size[0]]

        # Calculate the mean RGB values of the reference region - image white baseline value
        mean_reference = np.mean(reference_region, axis=(0, 1))

        # Scaling factors for each channel
        scale_factors = 255.0 / mean_reference

        # Apply white balancing to the entire image by multiplying the image to the scale factor
        balanced_image = cv.merge([cv.multiply(image[:, :, i], scale_factors[i]) for i in range(3)])

        # Clip the values to the valid range [0, 255]
        balanced_image = np.clip(balanced_image, 0, 255).astype(np.uint8)

        #cv.rectangle(balanced_image, reference_top_left, (reference_top_left[0] + reference_size[0], reference_top_left[1] + reference_size[1]), (0, 255, 0), 2)
        
        return balanced_image





""" DEPRECATED FUNCTIONS """
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