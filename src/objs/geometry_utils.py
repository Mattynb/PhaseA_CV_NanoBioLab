
from math import sqrt
import cv2 as cv
import numpy as np
from cv2.typing import MatLike

# Euclidian Distance
def distance(p1:float, p2:float):
    """
    p1 = (x1,y1)
    p2 = (x2,y2)
    """
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def contour_is_circular(contour: MatLike):
    """
    ### Contour is circular
    ---------------
    Function that checks if a contour is circular.
    
    #### Args:
    * contour: Contour of the object in the image.
    """

    # Approximate the contour
    perimeter = cv.arcLength(contour, True)
    area = cv.contourArea(contour)
    circularity = 4 * np.pi * (area / (perimeter ** 2))

    # Check the circularity
    check_1 = False
    if 0.6 < circularity < 1.4:
        # This contour is close to a circle
        check_1 = True

    # Fit a bounding rectangle and check the aspect ratio
    x, y, w, h = cv.boundingRect(contour)
    aspect_ratio = float(w) / h
    check_2 = False
    if 0.6 < aspect_ratio < 1.4:
        # The contour is close to being contained in a square
        check_2 = True

    # Minimum enclosing circle
    (x, y), radius = cv.minEnclosingCircle(contour)
    circle_area = np.pi * (radius ** 2)
    check_3 = False
    if 0.6 < (area / circle_area) < 1.4:
        # The area of the contour is close to that of the enclosing circle
        check_3 = True
    
    if check_1 and check_2 and check_3:
        return True

    return False

# checks if a combination of points are arranged in the shape of a square 
def is_arranged_as_square(points:list[tuple]):
    """
    checks if a combination of points are arranged in the shape of a square
    ----------
    points= combination of 4 points (x,y)
    """
    
    # Assuming points is a list of four (x, y) tuples
    # Calculate distances between each pair of points
    dists = []
    for i in range(4):
        for j in range(i + 1, 4):
            dists.append(distance(points[i], points[j]))
    
    #dists = [distance(points[i], points[j]) for i in range(4) for j in range(i+1, 4 - i)]
    dists.sort()
    """ if (
        np.isclose(dists[0], dists[1], atol=0.02, rtol=0.02) 
        and np.isclose(dists[1], dists[2], atol=0.02, rtol=0.02) 
        and np.isclose(dists[2], dists[3], atol=0.02, rtol=0.02) 
        and np.isclose(dists[4], dists[5], atol=0.02, rtol=0.02)
    ):
        print(dists)"""
    
    # Check for four sides of equal length and two equal diagonals
    return (
        np.isclose(dists[0], dists[1], atol=0.02, rtol=0.02) 
        and np.isclose(dists[1], dists[2], atol=0.02, rtol=0.02) 
        and np.isclose(dists[2], dists[3], atol=0.02, rtol=0.02) 
        and np.isclose(dists[4], dists[5], atol=0.02, rtol=0.02)
    )


# Finds center point of contour 
def find_center_of_contour(contour: MatLike):   
    """
    Finds Center point of a single contour
    ---------
    contour: single contour

    """
    M = cv.moments(contour)  

    # avoiding division by zero
    if M["m00"] != 0:
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])
    
        return (x, y)
    else:
        
        return None

# Finds center point of points
def find_center_of_points(points: list[tuple]):
    """
    Finds Center point of a list of points
    ---------
    points: list of points

    """
    x = 0
    y = 0

    for point in points:
        x += point[0]
        y += point[1]

    return (x//len(points), y//len(points))

# Translates the x,y coordinates to the equivalent index of grid_ds.
def xy_to_index(Grid , x:int , y:int):
    """
    ### XY to index
    ---------------
    Function that translates the x,y coordinates to the equivalent index of grid_ds.
    
    #### Args:
    * x: x coordinate of the point
    * y: y coordinate of the point
    * Grid: Grid object

    #### Returns:
    * index of the point in the grid_ds
    """

    x_index = int(round(x // Grid.SQUARE_LENGTH))
    y_index = int(round(y // Grid.SQUARE_LENGTH))

    return (min(x_index, Grid.MAX_INDEX), min(y_index, Grid.MAX_INDEX))

# Same as above but taking into consideration the skewing that happens near the outter squares.
def xy_to_index_skewed(Grid, x: int, y: int, a:float):

    middle_index_tl_x = (Grid.SQUARE_LENGTH * Grid.MAX_INDEX)/2
    middle_index_tl_y = (Grid.SQUARE_LENGTH * Grid.MAX_INDEX)/2
    
    index_x, index_y = xy_to_index(Grid, x , y)

    offset_x = int(abs(middle_index_tl_x - index_x)**a)
    offset_y = int(abs(middle_index_tl_y - index_y)**a)

    index_x_skewed = int(round(x // (Grid.SQUARE_LENGTH + offset_x)))
    index_y_skewed = int(round(y // (Grid.SQUARE_LENGTH + offset_y)))

    return (min(index_x_skewed, Grid.MAX_INDEX), min(index_y_skewed, Grid.MAX_INDEX))

# Translates the index to the equivalent x,y coordinates of grid_ds top left point.   
def index_to_xy(Grid, x_index:int, y_index:int):
    """
    ### Index to XY
    ---------------
    Function that translates the index to the equivalent x,y coordinates of grid_ds tl point.

    #### Args:
    * x_index: x index of the point
    * y_index: y index of the point
    * grid_ds: Grid object

    #### Returns:
    * x,y coordinates of the top left point of the square
    """
   
    x = (x_index) * Grid.SQUARE_LENGTH
    y = (y_index) * Grid.SQUARE_LENGTH

    return (x, y) # top left point of square