import cv2 as cv
import numpy as np

class GPUMorphologicalTransformer():
    """"
    ## GPUMorphologicalTransformer
    
    This class is responsible for applying morphological transformations to an image using the GPU.
    
    ### Methods
    - `process_image(image: np.ndarray) -> np.ndarray`
        - This method applies morphological transformations to the given image and returns the processed image.
    
    ### Example
    ```python
    import cv2 as cv
    import src.objs.image.processors.gpu_morphological_transformer as gpu_morphological_transformer

    image = cv.imread('path/to/image.jpg')
    processed_image = gpu_morphological_transformer.GPUMorphologicalTransformer.apply_morph(image)
    ```
    """
    @staticmethod
    def apply_morph(image: np.ndarray) -> np.ndarray:
        """This method applies morphological transformations to the given image and returns the processed image."""

        # Upload the image to the GPU
        gpu_img = cv.cuda.GpuMat()
        gpu_img.upload(image)
        gpu_img = cv.cuda.cvtColor(gpu_img, cv.COLOR_BGR2GRAY)

        # Apply morphological transformations to the image
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
        morph = cv.cuda.createMorphologyFilter(cv.MORPH_OPEN, gpu_img.type(), kernel, iterations=3)
        gpu_img = morph.apply(gpu_img)

        # Download the processed image from the GPU and return it
        gpu_img = cv.cuda.cvtColor(gpu_img, cv.COLOR_GRAY2BGR)
        img = gpu_img.download()

        return img
