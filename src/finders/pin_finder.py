from finders.rgb_finder import RGB_Finder
from obj.blocks import Block
from obj.pins import Pin


class PinFinder:
    def __init__(self, potential_pins: Pin, area_of_ref_square:float, thickness_of_grid_edge:float, coord_of_top_right_corner:tuple[int,int]) -> list(Block):
        
        # check alignment of pins within an area of the size of the black square

        # start from top right of the grid.
        # go through each spot in the grid and check which pins are within that x,y,w,h.
            # if there are 4 pins that are aligned (or very close to being aligned), there is your pins
        pins = []


        # now you can find the block by finding the center of the pins 
        #   ___________     
        #  |           | 
        #  |  a     b  |
        #  |           |
        #  |  c     d  |
        #  |___________|
        # 
        #  x = ax + ((bx - ax)/2)
        #  y = ay + ((cy - ay)/2)  
        #  lenght = sqrt(area_of_square)
        #
        #  remembering that x grows to the right and y grows to the bottom 
        blocks = []


        return blocks

