


class Image:
    def __init__(self, id, image):
        self.id = id
        
        self.img_og = image
        self.img_std_size = self.resize_2_std()
        #self.img_std = self.pre_process()  # std == processed
        
        #self.ref_squares = self.find_ref_squares()  # [coords1, cords2, ... , coords4]
        #self.grid = None
        #self.edges = []
        #self.blocks = []


    def pre_process(self):
        img = self.img_og 
        
        img = self.angle_fix(img)
        img = self.isolate_foreground(img) # now you only have the grid 
        self.grid = img
        img = self.resize_2_std(img) 

        return img


    def angle_fix(self):
        """ 
        Not Finished yet.\n
        Be aware that the copied part of the algorithm assumes that tl, tr, br, bl 
        refer to the whole grid rather than individual squares
        """
        from numpy import sqrt, float32
        from cv2 import getPerspectiveTransform, warpPerspective, INTER_LINEAR

        for i in range (4):
            ref_sq = self.ref_squares[i]
            x,y,w,h = ref_sq
            tl = (x,y) 
            tr = (x+w, y) 
            br = (x, y+h)
            bl = (x+w, y+h)
        
        
        # Finding the maximum width.
        widthA = sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        # Finding the maximum height.
        heightA = sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        # Final destination co-ordinates.
        destination_corners = [[0, 0], [maxWidth, 0], [maxWidth, maxHeight], [0, maxHeight]]

        # Getting the homography.
        #M = getPerspectiveTransform(float32(corners), float32(destination_corners))

        # Perspective transform using homography.
        #final = warpPerspective(self.img_og, M, (destination_corners[2][0], destination_corners[2][1]), flags=INTER_LINEAR)

        


    def find_ref_squares(self):
        ref_squares = []
        
        # use adaptive filtering to leave only the black squares, there should be exactly four
    
        # record the coordinates of each square edge
        # now you can calculate the lenght and area in pixels of each square
        ...
        return ref_squares # [coords1, cords2, ... , coords4], coords = (x, y, L)

    def isolate_foreground(self):
        ...

    def resize_2_std(self, i = 0):
        from cv2 import resize

        if i == 0:
            img = self.img_og

        self.img_std_size = resize(img, (500,500))

def Image_loader(path_to_images: str) -> list[Image]:
    """Loads all the images in a path as Image"""

    from glob import glob
    from cv2 import imread

    
    types = ('.png', '.jpg', '.jpeg')

    # reading single image if path is only one image
    end = path_to_images[-4:]
    if end in types or end == 'jpeg': 
        return [Image(100, imread(path_to_images))]

    # reading all images of acceptable types from given directory 
    imgs = []
    for f_type in types:      
        imgs.extend([imread(file) for file in glob(f"{path_to_images}\*{f_type}")])
    
    # turning read images into Image
    Images = [Image( i + 100, imgs[i]) for i in range(len(imgs))]
    
    return Images 


if __name__ == '__main__':
    # Image_loader test
    from cv2 import imshow, waitKey, destroyAllWindows
    Images = Image_loader(r"C:\Users\Matheus\Desktop\NanoTechnologies_Lab\Phase A\data\img\block3.jpeg") 
    for i in Images:
        i.resize_2_std()
        imshow(str(i.id), i.img_std_size)
    waitKey(0)
    destroyAllWindows()



