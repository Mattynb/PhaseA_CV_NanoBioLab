import numpy as np

def get_rgb_avg_of_area(self, x, y, w, h):
        """ 
        ### Get RGB average of area
        ---------------
        Function that gets the average RGB of an area of the image.
        
        #### Args:
        * x: x coordinate of the top left point of the area
        * y: y coordinate of the top left point of the area
        * w: width of the area
        * h: height of the area
        
        #### Returns:
        * Average RGB of the area
        """
        
        # crop the image
        image_copy = self.img.copy()
        crop = image_copy[y:y+h, x:x+w]

        # get the average of each channel
        avg_color_per_row = np.average(crop, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        avg_color = np.uint8(avg_color)

        return avg_color        
