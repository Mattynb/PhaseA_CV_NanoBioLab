from pins import Pin
from results import Result

class Block():
    def __init__(self, location: tuple[int], pins: set[Pin], test_result: Result):

        # (x, y, length)
        self.x, self.y, self.w, self.h = location  # using length because w, h should be the same (square)
        
        self.pin = pins
        
        self.results = test_result
        
        self.encoding_sequence = self.encoding_finder(pins) 

        
    
    def encoding_finder(pins):
        ...