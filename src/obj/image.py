def Image_loader(path_to_images):
    images = []
    
    ...

    return images


class Image:
    def __init__(self, id, image):
        self.id = id
        
        self.img_og = image
        self.img_std = self.pre_process()  # std == processed
        
        self.ref_squares = self.find_ref_squares()  # [coords1, cords2, ... , coords4]
        self.grid = None
        self.edges = []
        self.blocks = []


    def pre_process(self):
        img = self.og_img 
        
        img = self.angle_fix(img)
        img = self.isolate_foreground(img) # now you only have the grid 
        self.grid = img
        img = self.resize_2_std(img) 

        return img


    def angle_fix(self):
        for ref_sq in self.ref_squares:
            tl,tr,br,bl = ...
        
        """
        (tl, tr, br, bl) = pts
        # Finding the maximum width.
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
        # Finding the maximum height.
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
        # Final destination co-ordinates.
        destination_corners = [[0, 0], [maxWidth, 0], [maxWidth, maxHeight], [0, maxHeight]]
        """

        

        ...

    def find_ref_squares(self):
        ref_squares = []
        
        # use adaptive filtering to leave only the black squares, there should be exactly four
    
        # record the coordinates of each square edge
        # now you can calculate the lenght and area in pixels of each square
        ...
        return ref_squares # [coords1, cords2, ... , coords4], coords = (x, y, L)

    def isolate_foreground(self):
        ...

    def resize_2_std(self):
        ...
    
    def load(self, path_to_images):

        return


