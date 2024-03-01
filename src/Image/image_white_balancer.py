import numpy as np
import cv2 as cv

class WhiteBalanceAdjuster:
    @staticmethod
    def adjust( image: np.ndarray, 
                reference_region: tuple[int, int, int, int] = (62, 80, 20, 20)
            ) -> np.ndarray:

        """
        Adjust the white balance of the image.
        Args:
            image: The image to adjust.
            reference_region: The top-left coordinates and size of the reference region.
        Returns:
            The white-balanced image.
        """

        reference_top_left, reference_size = reference_region[:2], reference_region[2:]
        #cv.rectangle(balanced_image, reference_top_left, (reference_top_left[0] + reference_size[0], reference_top_left[1] + reference_size[1]), (0, 255, 0), 2) 

        # Create the reference 10x10 square for the reference region for white balancing
        reference_region = image[reference_top_left[1]:reference_top_left[1] + reference_size[1],
                                reference_top_left[0]:reference_top_left[0] + reference_size[0]]

        # Calculate the mean RGB values of the reference region - image white baseline value
        mean_reference = np.mean(reference_region, axis=(0, 1))

        # Scaling factors for each channel
        scale_factors = 255.0 / mean_reference

        # Apply white balancing to the entire image by multiplying the image to the scale factor
        balanced_image = cv.merge([cv.multiply(image[:, :, i], scale_factors[i]) for i in range(3)])

        # Clip the values to the valid range [0, 255]
        balanced_image = np.clip(balanced_image, 0, 255).astype(np.uint8)

        
        return balanced_image