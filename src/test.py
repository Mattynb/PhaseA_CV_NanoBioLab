import time
import cv2 as cv
import numpy as np

time1 = time.time()
file = r"data\New_images_022624\IMG_5514.JPEG"
img = cv.imread(file)
img = cv.resize(img, (0, 0), fx=0.5, fy=0.5)

# APPLYING MORPHOLOGICAL TRANSFORMATIONS TO HIGHLIGHT THE GRID
# Note: This part is done on CPU, consider using GPU for morphological operations if your OpenCV version supports it
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
img = cv.morphologyEx(img, cv.MORPH_OPEN, kernel, iterations=3)

# Uploading the image to GPU memory for further processing
gpu_img = cv.cuda_GpuMat()
gpu_img.upload(img)

# For GPU-accelerated operations, ensure operations are done on gpu_img

# Example of converting to grayscale using CUDA
gpu_gray = cv.cuda.cvtColor(gpu_img, cv.COLOR_BGR2GRAY)

# Since cv.cuda.CannyEdgeDetector is not directly accessible like this, you need to use cv.cuda.createCannyEdgeDetector()
# and then use it to detect edges. Note: This is a corrected approach for edge detection.
canny_detector = cv.cuda.createCannyEdgeDetector(0, 200)
gpu_canny = canny_detector.detect(gpu_gray)

# To perform operations like findContours, you need to download the image from GPU memory back to CPU memory
canny_cpu = gpu_canny.download()

# CONTOUR DETECTION
# Note: Contour detection is not available on GPU, so it's performed on the CPU
con = np.zeros_like(img)  # Blank canvas for drawing contours
contours, hierarchy = cv.findContours(canny_cpu, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
# Keeping only the largest detected contour
if contours:
    contours = max(contours, key=cv.contourArea)
    # Drawing the largest contour on the blank canvas
    cv.drawContours(con, [contours], -1, (0, 255, 0), 3)

cv.imshow("img", img)
cv.imshow("con", con)
cv.waitKey(0)
cv.destroyAllWindows()

time2 = time.time()
print(f"Processing time: {time2 - time1} seconds")
