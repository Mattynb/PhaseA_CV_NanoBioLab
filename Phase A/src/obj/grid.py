from blocks import Block

class Grid():
    def __init__(self, location: tuple[int], blocks: set[Block], grid_map: list[list[bool]]):
        
        # (x, y, length)
        self.x, self.y, self.w, self.h = location  # using length because w, h should be the same (square)

        self.blocks = blocks
    
        self.grid_map = grid_map 
        
        """
        ex of a grid_map representing a 4x4 grid with 4 blocks:
        [
            [0, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 0, 0]
        ]
        """
