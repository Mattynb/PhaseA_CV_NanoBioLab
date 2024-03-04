import cv2 as cv
import numpy as np

class GPUMorphologicalTransformer(ImageProcessor):
    def process_image(self, image: np.ndarray) -> np.ndarray:
        gpu_img = self.upload_to_gpu(image)
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
        morph = cv.cuda.createMorphologyFilter(cv.MORPH_OPEN, gpu_img.type(), kernel, iterations=3)
        processed_gpu_img = morph.apply(gpu_img)
        return self.download_from_gpu(processed_gpu_img)
    
    def upload_to_gpu(self, image: np.ndarray) -> cv.cuda_GpuMat:
        gpu_img = cv.cuda_GpuMat()
        gpu_img.upload(image)
        return gpu_img

    def download_from_gpu(self, gpu_img: cv.cuda_GpuMat) -> np.ndarray:
        return gpu_img.download()