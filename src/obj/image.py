from os import path
import cv2 as cv
import numpy as np

class Image:
    def __init__(self, id, image):
        self.id = id
        
        self.img_og = image
        self.img_std_size = self.resize_2_std(image)
        self.ref_squares = self.find_ref_squares(self.img_std_size) #self.img_std_size) # [coords1, cords2, ... , coords4]
        
        corners = self.find_grid() #self.grid
        self.img_std_angle = self.angle_fix(corners)

        #self.img_std = self.pre_process()  # std == processed
    
        #self.blocks = []


    def pre_process(self):
        img = self.img_og 
        
        img = self.angle_fix(img)
        img = self.isolate_foreground(img) # now you only have the grid 
        self.grid = img
        img = self.resize_2_std(img) 

        return img

    def find_grid(self):
        # Finding the corners of the grid.
        tl,tr,bl,br = 0,0,0,0
        for i in range (0, 4):
            ref_sq = self.ref_squares[i]  # ref_squares is in order: [br, bl, tr, tl]
            x,y,w,h = ref_sq

            if i == 0:
                bl = (x -(0.12*w), y + h+(0.12*h))

            if i == 1:
                br = (x + w +(0.12*w), y + h +(0.12*h))

            if i == 2:
                tl = (x -(0.12*w), y -(0.12*h))
              
            if i == 3: 
                tr = (x + w +(0.12*w), y -(0.12*h))      
                
        corners = [tl, tr, br, bl]

        # Visuals
        """
        print(corners)
        cv.line(self.img_std_size, tl, tr, (255,255,0), 2)
        cv.line(self.img_std_size, tr, br, (0,255,0), 2)
        cv.line(self.img_std_size, br, bl, (0,255,255), 2)
        cv.line(self.img_std_size, bl, tl, (0,0,255), 2)
        cv.imshow('img', self.img_std_size)
        cv.waitKey(0)
        cv.destroyAllWindows()
        #"""
        return corners

    def angle_fix(self, corners):
        """
        Not Finished yet.\n
        Be aware that the copied part of the algorithm assumes that tl, tr, br, bl 
        refer to the whole grid rather than individual squares
        """
        
        (tl, tr, bl, br) = corners 
        
        # Finding the maximum width.
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        # Finding the maximum height.
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        # Final destination co-ordinates.
        destination_corners = [[0, 0], [maxWidth, 0], [maxWidth, maxWidth], [0, maxWidth]]

        # Getting the homography.
        M = cv.getPerspectiveTransform(np.float32(corners), np.float32(destination_corners))

        # Perspective transform using homography.
        final = cv.warpPerspective(self.img_std_size, M, (destination_corners[2][0], destination_corners[2][1]), flags=cv.INTER_LINEAR)

        cv.imshow('img', final)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def find_ref_squares(self, src_img):
        # use threshold to leave only the black squares, there should be exactly four
        src_img = cv.cvtColor(src_img, cv.COLOR_RGB2GRAY)
        src_img = cv.GaussianBlur(src_img, (5,5), 9)
        #src_img =cv.medianBlur(src_img, 5) # medianBlur is better for removing salt and pepper noise
        #src_img =cv.blur(src_img, (5,5)) # blur is better for removing gaussian noise
        #src_img =cv.stackBlur(src_img, 5) # stackBlur is better for removing gaussian noise
        #src_img =cv.bilateralFilter(src_img, 5, 50, 50) # bilateralFilter is better for removing gaussian noise
        _, src_img = cv.threshold(src_img, 50, 255, cv.THRESH_BINARY)
        edges = cv.Canny(src_img, 150, 150)
        
        #"""
        cv.imshow('img', src_img)
        cv.waitKey(0)
        cv.destroyAllWindows()
        #"""
        contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        
        # Visuals
        img_std = self.img_std_size.copy()
        
        # find the four biggest squares
        ref_squares = [(0,0,0,0),(0,0,0,0),(0,0,0,0),(0,0,0,0)]
        for contour in contours:
            x, y, w, h = cv.boundingRect(contour)

            # if the contour is too small, it's probably not a square
            if len(ref_squares) < 4 or w > min(ref_squares, key=lambda x: x[2])[2]:     # x is a tuple (x,y,w,h), x[2] is the width
                ref_squares.remove(min(ref_squares, key=lambda x: x[2]))
                ref_squares.append((x,y,w,h))

        # paint the squares on the image
        #"""
        for x,y,w,h in ref_squares:
            cv.rectangle(img_std, (x,y), (x+w, y+h), (255,0,0), 2)
        
            
        cv.imshow('img', img_std)
        cv.waitKey(0)
        cv.destroyAllWindows()
            #"""

        # record the coordinates of each square edge
        # now you can calculate the lenght and area in pixels of each square
    
        return ref_squares # [coords1, cords2, ... , coords4], coords = (x, y, L)

    def resize_2_std(self, img):
        h, w = img.shape[:2]
        return cv.resize(img, (int(w*0.3), int(h*0.3)), interpolation=cv.INTER_NEAREST)


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
        imgs.extend([imread(file) for file in glob(f"{path_to_images}*{f_type}")])
    
    # turning read images into Image
    Images = [Image( i + 100, imgs[i]) for i in range(len(imgs))]
    
    return Images 


if __name__ == '__main__':
    image = Image_loader(r"C:\Users\Matheus\Desktop\NanoTechnologies_Lab\Phase A\data\img\block_with_refSq_") 
    I = image[0]

    cv.waitKey(0)
    cv.destroyAllWindows()



