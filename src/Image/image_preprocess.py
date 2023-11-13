import cv2 as cv

def pre_process2(scaned_image): #find_pins(scaned_image)?
    """ 
    The pins are the only part of the image that isnt "black" or "white".
    Therefore you could potentially look for the colored pins by looking for the pixels that arent black or white threshold.
    e.g if pixel rgb avg value is > 10 and < 245 then its a pin
    """

    gray = cv.cvtColor(scaned_image, cv.COLOR_BGR2GRAY)
    at = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 3, 5)
    at = cv.GaussianBlur(at, (5, 5), 1) 
    at = cv.blur(at, (3, 3))
    _, no_white = cv.threshold(at, 150, 255, cv.THRESH_BINARY)
    
    #"""
    cv.imshow('no_white', no_white)
    cv.waitKey(0)
    cv.destroyAllWindows()
    #"""

    edges = cv.Canny(no_white, 100, 200)
    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    
    
    for contour in contours:
        ratio = scaned_image.shape[1] * 0.01
        plus_minus = round(scaned_image.shape[1] * 0.0025)

        #print(f"{ratio} : {plus_minus}")
        x, y, w, h = cv.boundingRect(contour)
        if (h, w) >= (ratio - plus_minus, ratio - plus_minus) and (h,w) <= (ratio + plus_minus, ratio + plus_minus):        
            #cv.rectangle(scaned_image, (x, y), (x+w, y+h), (0, 255, 0), 2)        
            cv.circle(scaned_image, tuple(contour[0][0]), int(w/2), (0, 0, 255), 1)
 
    cv.imshow('contour', scaned_image)
    cv.waitKey(0)
    cv.destroyAllWindows()
 
def pre_process(scaned_image):
    import cv2
    import numpy as np

    scaned_image_copy = scaned_image.copy()

    # Convert the image to HSV color space
    img_hsv = cv2.cvtColor(scaned_image_copy, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the color you want to isolate
    lower_color = np.array([30, 28, 30])
    upper_color = np.array([215, 215, 215])

    # Create a mask using the inRange function
    color_mask = cv2.inRange(img_hsv, lower_color, upper_color)
    
    cv.imshow('img_hsv', img_hsv)
    cv.imshow('mask', color_mask)
    cv.waitKey(0)
    cv.destroyAllWindows()

   

    # Apply the mask to the original image using bitwise_and
    result = cv2.bitwise_and(scaned_image_copy, img_hsv, mask=color_mask)
    
    edges = cv.Canny(result, 100, 200)
    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    
       
    xx = scaned_image.shape[0]
    yy = scaned_image.shape[1] 
    pin_ratio = round(scaned_image.shape[1] * 0.01)
    edge_ratio = round(scaned_image.shape[1] * 0.01)
    plus_minus = round(scaned_image.shape[1] * 0.008)

    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)

        # checks if the contour is inside edges of the grid and if its around the size of a pin.
        if x > edge_ratio and y > edge_ratio: 
            if x+w < xx - edge_ratio and y+h < yy - edge_ratio:
                if  h <= pin_ratio + plus_minus and w <= pin_ratio + plus_minus:   
                    cv.rectangle(scaned_image, (x, y), (x+w, y+h), (0, 255, 0), 1)

    cv.imshow('contour', scaned_image)
    cv.imshow('result', result)
    cv.waitKey(0)
    cv.destroyAllWindows()