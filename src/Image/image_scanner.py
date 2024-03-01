import cv2 as cv
import numpy as np

class ImageScanner:
        @classmethod
        def scan(cls, image_og: np.ndarray)->np.ndarray:
                """
                ### Image scanner
                Scans the image and returns the scanned image. It does that by first removing the background, then finding the corners of the grid and finally rearranging the corners to get a straight image.

                #### Args:
                std_size_img: image to be scanned

                #### Returns:
                Scanned image

                #### References:
                https://learnopencv.com/automatic-document-scanner-using-opencv/
                """
                
                # copy of the image to be scanned (to not mess with the original)
                img = image_og.copy()
                """
                cv.imshow('og', img)
                cv.waitKey(0)  
                cv.destroyAllWindows()
                #"""

                
                # APPLYING MORPHOLOGICAL TRANSFORMATIONS TO HIGHLIGHT THE GRID
                kernel = np.ones((5,5), np.uint8)
                img = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel, iterations=3)  
                """
                cv.imshow('morph', img)
                cv.waitKey(0)  
                cv.destroyAllWindows()
                #"""

                # GETTING RID OF THE BACKGROUND THROUGH MASKING + GRABCUT ALGORITHM
                mask = np.zeros(img.shape[:2],np.uint8)
                bgdModel = np.zeros((1,65),np.float64)
                fgdModel = np.zeros((1,65),np.float64)
                rect = (20,20,img.shape[1]-20,img.shape[0]-20)
                cv.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv.GC_INIT_WITH_RECT)
                mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
                img = img*mask2[:,:,np.newaxis]
                """
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
                """
                cv.imshow('contour', con)
                cv.waitKey(0)  
                cv.destroyAllWindows()
                #"""

                # DETECTING THE CORNERS OF THE GRID
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
                corners = cls.order_points(corners)
        
                # Displaying the corners.
                for index, c in enumerate(corners):
                        character = chr(65 + index)
                        cv.putText(con, character, tuple(c), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv.LINE_AA)
                """
                cv.imshow('contour', con)
                cv.waitKey(0)  
                cv.destroyAllWindows()
                #"""

                # REARRANGING THE CORNERS 
                destination_corners = cls.find_dest(corners)

                # Getting the homography. (aka scanning the image)
                M = cv.getPerspectiveTransform(np.float32(corners), np.float32(destination_corners))
                # Perspective transform using homography.
                final = cv.warpPerspective(image_og, M, (destination_corners[2][0], destination_corners[2][1]), flags=cv.INTER_LINEAR)
                """
                cv.imshow('final', final)
                cv.waitKey(0)
                cv.destroyAllWindows()
                #"""
        
                return final

        @classmethod
        def find_dest(cls, pts: list)->list:
                """
                ### Find destination
                Finds the destination coordinates for the image to be scanned.

                #### Args:
                pts: points to be rearranged

                #### Returns:
                Rearranged points
                """
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
                """
                ### Order points
                Orders the points in a clockwise manner (starting from top-left)
                
                #### Args:
                pts: points to be rearranged
                
                #### Returns:
                Rearranged points
                """
                # Initialising a list of coordinates that will be ordered.
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


        