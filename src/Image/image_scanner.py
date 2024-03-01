import re
import cv2 as cv
from matplotlib.pyplot import contour
import numpy as np

class ImageScanner:
        @classmethod
        def scan(cls, image_og: np.ndarray)->np.ndarray:
                # copy of the image to be scanned (to not mess with the original)
                img = image_og.copy()

                # GPU acceleration
                gpu_img = cv.cuda_GpuMat()
                gpu_img.upload(img)

                img = cls.morphological_transform(img)
                img = cls.remove_background(img)
                contours = cls.find_contours(img)
                corners = cls.detect_corners(contours, img)
                final_image = cls.perspective_transform(image_og, corners)
                return final_image
        
        @staticmethod
        def morphological_transform(img: np.ndarray)->np.ndarray:
                # APPLYING MORPHOLOGICAL TRANSFORMATIONS TO HIGHLIGHT THE GRID
                kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
                img = cv.cuda.morphologyEx(img, cv.MORPH_CLOSE, kernel, iterations=3)  
                return img

        @staticmethod
        def remove_background(img: np.ndarray)->np.ndarray:
                # GETTING RID OF THE BACKGROUND THROUGH MASKING + GRABCUT ALGORITHM
                mask = np.zeros(img.shape[:2],np.uint8)
                bgdModel = np.zeros((1,65),np.float64)
                fgdModel = np.zeros((1,65),np.float64)
                rect = (20,20,img.shape[1]-20,img.shape[0]-20)
                cv.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv.GC_INIT_WITH_RECT)
                mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
                return img*mask2[:,:,np.newaxis]

        @staticmethod
        def find_contours(img: np.ndarray)->np.ndarray:
                # EDGE DETECTION
                gray = cv.cuda.cvtColor(img, cv.COLOR_BGR2GRAY)
                gray = cv.cuda.GaussianBlur(gray, (11, 11), 0)
                canny = cv.cuda.Canny(gray, 0, 200)
                canny = cv.dilate(canny, cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5)))
                canny = canny.download()

                # CONTOUR DETECTION
                con = np.zeros_like(img)  # Blank canvas.
                # Finding contours for the detected edges.
                contours, hierarchy = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
                # Keeping only the largest detected contour.
                return sorted(contours, key=cv.contourArea, reverse=True)[:5]
               
                """
                cv.imshow('contour', con)
                cv.waitKey(0)  
                cv.destroyAllWindows()
                #"""

        @classmethod
        def detect_corners(cls, contours: list, img:np.ndarray)->np.ndarray:
                # DETECTING THE CORNERS OF THE GRID

                # Loop over the contours.
                for c in contours:
                        # Approximate the contour.
                        epsilon = 0.02 * cv.arcLength(c, True)
                        corners = cv.approxPolyDP(c, epsilon, True)
                        # If our approximated contour has four points
                        if len(corners) == 4:
                                break
                
                # Sorting the corners and converting them to desired shape.
                corners = sorted(np.concatenate(corners).tolist())
                corners = cls.order_points(corners)

                return corners

        
        @classmethod
        def perspective_transform(cls, img: np.ndarray, corners: list)->np.ndarray:
                # REARRANGING THE CORNERS 
                destination_corners = cls.find_dest(corners)
                
                # Getting the homography. (aka scanning the image)
                M = cv.getPerspectiveTransform(np.float32(corners), np.float32(destination_corners))
                
                # Perspective transform using homography.
                final = cv.warpPerspective(img, M, (destination_corners[2][0], destination_corners[2][1]), flags=cv.INTER_LINEAR)
                cv.imshow('final', final)
                cv.waitKey(0)
                cv.destroyAllWindows()
                #"""
        
                return final

        @classmethod
        def find_dest(cls, pts: list)->list:
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
                return cls.order_points(destination_corners)

        @staticmethod
        def order_points(pts: list)->list:
                # Initialising a list of coordinates that will be ordered.
                rect = np.zeros((4, 2), dtype='float32')
                pts = np.array(pts)
                s = pts.sum(axis=1)
        
                # Top-left point will have the smallest sum.
                rect[0] = pts[np.argmin(s)]
        
                # Bottom-right point will have the largest sum.
                rect[2] = pts[np.argmax(s)]
        
                # Computing the difference between the points.
                diff = np.diff(pts, axis=1)

                # Top-right point will have the smallest difference.
                rect[1] = pts[np.argmin(diff)]
                
                # Bottom-left will have the largest difference.
                rect[3] = pts[np.argmax(diff)]
                
                # Return the ordered coordinates.
                return rect.astype('int').tolist()


        