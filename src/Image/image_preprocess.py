import cv2 as cv
from sympy import Le


def pre_process(scaned_image): #find_pins(scaned_image)?
    """ 
    The pins are the only part of the image that isnt "black" or "white".
    Therefore you could potentially look for the colored pins by looking for the pixels that arent black or white threshold.
    e.g if pixel rgb avg value is > 10 and < 245 then its a pin
    """

    gray = cv.cvtColor(scaned_image, cv.COLOR_BGR2GRAY)
    _, no_white = cv.threshold(scaned_image, 150, 255, cv.THRESH_BINARY, gray)
    
    #"""
    cv.imshow('no_white', no_white)
    cv.waitKey(0)
    cv.destroyAllWindows()
    #"""
    
    edges = cv.Canny(no_white, 100, 200)
    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    
    
    for contour in contours:
        ratio = scaned_image.shape[1] * 0.01
        plus_minus = scaned_image.shape[1] * 0.005

        x, y, w, h = cv.boundingRect(contour)
        if (h, w) > (ratio - plus_minus, ratio - plus_minus) and (h,w) < (ratio + plus_minus, ratio + plus_minus):        
            cv.rectangle(scaned_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    cv.imshow('contour', scaned_image)
    cv.waitKey(0)
    cv.destroyAllWindows()
 

#if __name__ == '__main__':
