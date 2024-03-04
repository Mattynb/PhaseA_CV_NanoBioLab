import cv2 as cv
import numpy as np

class ImageScanner:
        @classmethod
        def scan(cls, image_og: np.ndarray)->np.ndarray:
                # copy of the image to be scanned (to not mess with the original)
                img = image_og.copy()

                # GPU acceleration for faster processing
                gpu_img = cv.cuda_GpuMat()
                gpu_img.upload(img)
                gpu_img = cv.cuda.cvtColor(gpu_img, cv.COLOR_BGR2GRAY)
                gpu_img = cls.morphological_transform(gpu_img)
                 
                # Only works with CPU
                cpu_img = gpu_img.download()
                cpu_img = cls.remove_background(cpu_img)
                
                # Uploading the image to the GPU again for faster processing
                gpu_img.upload(cpu_img)
                contours = cls.find_contours(gpu_img)
                corners = cls.detect_corners(contours, cpu_img)
                final_image = cls.perspective_transform(image_og, corners)
                
                return final_image
        
        @staticmethod
        def morphological_transform(gpu_img: cv.cuda_GpuMat)->  cv.cuda_GpuMat:
                # APPLYING MORPHOLOGICAL TRANSFORMATIONS TO HIGHLIGHT THE GRID
                kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
                morph = cv.cuda.createMorphologyFilter(cv.MORPH_OPEN, gpu_img.type(), kernel, iterations=3)
                gpu_img = morph.apply(gpu_img)
                return gpu_img

        @staticmethod
        def remove_background(img: np.ndarray)->np.ndarray:
                # GETTING RID OF THE BACKGROUND THROUGH MASKING + GRABCUT ALGORITHM
                mask = np.zeros(img.shape[:2],np.uint8)
                bgdModel = np.zeros((1,65),np.float64)
                fgdModel = np.zeros((1,65),np.float64)
                rect = (20,20,img.shape[1]-20,img.shape[0]-20)
                img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
                cv.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv.GC_INIT_WITH_RECT)
                mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
                return img*mask2[:,:,np.newaxis]

        @staticmethod
        def find_contours(gpu_img: cv.cuda_GpuMat)->list:
                # EDGE DETECTION
                gpu_img = cv.cuda.cvtColor(gpu_img, cv.COLOR_BGR2GRAY)
                gpu_blurred = cv.cuda.createGaussianFilter(gpu_img.type(), -1, (11, 11), 0).apply(gpu_img)
                
                detector = cv.cuda.createCannyEdgeDetector(0, 200)
                
                gpu_canny = detector.detect(gpu_blurred)

                canny_cpu = gpu_canny.download()  # Downloading for CPU processing

                # CONTOUR DETECTION (CPU)
                contours, _ = cv.findContours(canny_cpu, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
                return sorted(contours, key=cv.contourArea, reverse=True)[:5]
                
        @classmethod
        def detect_corners(cls, contours: list, img:np.ndarray)->list:
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