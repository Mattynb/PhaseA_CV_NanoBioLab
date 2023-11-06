from os import path
import cv2 as cv
import numpy as np

class Image:
    def __init__(self, id, image):
        self.id = id
        
        self.img_og = image
        self.img_std_size = self.resize_2_std(image)
        
        self.img_std = self.scan()

        #self.img_std = self.pre_process()  # std == processed
    
        #self.blocks = []


    def pre_process(self):
        img = self.img_og 
        
        img = self.angle_fix(img)
        img = self.isolate_foreground(img) # now you only have the grid 
        self.grid = img
        img = self.resize_2_std(img) 

        return img

    def scan(self):
        """https://learnopencv.com/automatic-document-scanner-using-opencv/"""
        img = self.img_std_size.copy()
        #"""
        cv.imshow('og', img)
        cv.waitKey(0)  
        cv.destroyAllWindows()
        #"""

        
        # morphological operations ("removing" everything inside the grid)
        kernel = np.ones((5,5), np.uint8)
        img = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel, iterations=3)  
        #"""
        cv.imshow('morph', img)
        cv.waitKey(0)  
        cv.destroyAllWindows()
        #"""

        # GETTING RID OF THE BKG
        mask = np.zeros(img.shape[:2],np.uint8)
        bgdModel = np.zeros((1,65),np.float64)
        fgdModel = np.zeros((1,65),np.float64)
        rect = (20,20,img.shape[1]-20,img.shape[0]-20)
        cv.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv.GC_INIT_WITH_RECT)
        mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
        img = img*mask2[:,:,np.newaxis]
        #"""
        cv.imshow('no_bkg', img)
        cv.waitKey(0)  
        cv.destroyAllWindows()
        #"""

        # EDGE DETECTION
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        gray = cv.GaussianBlur(gray, (11, 11), 0)
        canny = cv.Canny(gray, 0, 200)
        canny = cv.dilate(canny, cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5)))

        # CONTOUR DETECTION
        con = np.zeros_like(img)  # Blank canvas.
        # Finding contours for the detected edges.
        contours, hierarchy = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
        # Keeping only the largest detected contour.
        page = sorted(contours, key=cv.contourArea, reverse=True)[:5]
        con = cv.drawContours(con, page, -1, (0, 255, 255), 3)
        #"""
        cv.imshow('contour', con)
        cv.waitKey(0)  
        cv.destroyAllWindows()
        #"""

        # DETECTING THE CORNERS
        con = np.zeros_like(img) # Blank canvas.
        # Loop over the contours.
        for c in page:
            # Approximate the contour.
            epsilon = 0.02 * cv.arcLength(c, True)
            corners = cv.approxPolyDP(c, epsilon, True)
            # If our approximated contour has four points
            if len(corners) == 4:
                break
        cv.drawContours(con, c, -1, (0, 255, 255), 3)
        cv.drawContours(con, corners, -1, (0, 255, 0), 10)
        # Sorting the corners and converting them to desired shape.
        corners = sorted(np.concatenate(corners).tolist())
        corners = self.order_points(corners)
        # Displaying the corners.
        for index, c in enumerate(corners):
            character = chr(65 + index)
            cv.putText(con, character, tuple(c), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv.LINE_AA)
        #"""
        cv.imshow('contour', con)
        cv.waitKey(0)  
        cv.destroyAllWindows()
        #"""

        # REARRANGING THE CORNERS
        destination_corners = self.find_dest(corners)

        # Getting the homography.
        M = cv.getPerspectiveTransform(np.float32(corners), np.float32(destination_corners))
        # Perspective transform using homography.
        final = cv.warpPerspective(self.img_std_size, M, (destination_corners[2][0], destination_corners[2][1]), flags=cv.INTER_LINEAR)
        #"""
        cv.imshow('final', final)
        cv.waitKey(0)
        cv.destroyAllWindows()
        #"""
        return final

    def find_dest(self, pts):
        # DESTINATION COORDINATES
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
        return self.order_points(destination_corners)
    
    def order_points(self, pts):
        '''Rearrange coordinates to order:
        top-left, top-right, bottom-right, bottom-left'''
        rect = np.zeros((4, 2), dtype='float32')
        pts = np.array(pts)
        s = pts.sum(axis=1)
        # Top-left point will have the smallest sum.
        rect[0] = pts[np.argmin(s)]
        # Bottom-right point will have the largest sum.
        rect[2] = pts[np.argmax(s)]
    
        diff = np.diff(pts, axis=1)
        # Top-right point will have the smallest difference.
        rect[1] = pts[np.argmin(diff)]
        # Bottom-left will have the largest difference.
        rect[3] = pts[np.argmax(diff)]
        # Return the ordered coordinates.
        return rect.astype('int').tolist()
  
    def resize_2_std(self, img, factor=0.3):
        h, w = img.shape[:2]
        return cv.resize(img, (int(w*factor), int(h*factor)), interpolation=cv.INTER_LINEAR)


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
    image = Image_loader(r"C:\Users\Matheus\Desktop\NanoTechnologies_Lab\Phase A\data\img\grid") 
    I = image[0]

    cv.waitKey(0)
    cv.destroyAllWindows()



