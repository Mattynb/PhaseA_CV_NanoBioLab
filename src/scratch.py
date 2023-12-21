from venv import create
from Image.image_class import Image
from Image.image_loader import Image_load
import Image.image_preprocess as pp
import numpy as np
import cv2 as cv
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt



def plot_rgb_values_of_contour(imge, contours):
    """ 
    ### Plot RGB values of a contour
    ---------------
    Function that plots the RGB values of a given contour in the image as a box and whisker plot.
    
    #### Args:
    * img: image array
    * contours: list of contours
    """
    img = imge.copy()

    mask = np.zeros_like(img)
    for contour in contours:
        cv.drawContours(mask, [contour], -1, (255, 255, 255), thickness=cv.FILLED)
    
    masked_img = cv.bitwise_and(img, mask)
    
    r_values = masked_img[:,:,0].flatten()
    g_values = masked_img[:,:,1].flatten()
    b_values = masked_img[:,:,2].flatten()

    # Remove 0 values
    r_values = r_values[r_values != 0]
    g_values = g_values[g_values != 0]
    b_values = b_values[b_values != 0]

    if len(r_values) > 1 or len(g_values) > 1 or len(b_values) > 1:
        # Sort RGB values
        rgb_values = np.column_stack((r_values, g_values, b_values))
        sorted_rgb_values = np.sort(rgb_values, axis=0)
        

        """cv.imshow('masked_img', masked_img)
        cv.waitKey(0)
        cv.destroyAllWindows()
    
        plt.figure()
        plt.boxplot(sorted_rgb_values, labels=['Red', 'Green', 'Blue'])
        plt.title('RGB Values Box and Whisker Plot')
        plt.xlabel('Channel')
        plt.ylabel('Value')
        plt.show()
        """
        
        # Calculate quartiles if sorted_rgb_values is not None
        quartile = np.percentile(sorted_rgb_values, [25, 75], axis=0)
        print(quartile)
        return quartile
        
    else:
        print("Not enough points to plot")

def create_excel_file(quartiles):
    """
    ### Create Excel file from quartiles values
    Creates an Excel file from the quartiles values.

    #### Args:
    quartiles: list of lists containing quartiles values
    """
    

    # Create a DataFrame from the quartiles values
    df = pd.DataFrame(quartiles, columns=['id', '25th Percentile', '75th Percentile'])

    # Save the DataFrame to an Excel file
    df.to_excel('quartiles.xlsx', index=False)



def main(path_to_imgs):
    """
    ### Main function
    Loads all the images in a folder and creates an Image object for each image.

    #### Args:
    path_to_imgs: path to image folder
    """

    # loading images
    images_og = Image_load(path_to_imgs)

    # creating Image objects
    id = 1
    quartiles = []
    for img in images_og:
        try:
            Image_i = Image(id, img, 0.4)
            print(f"Image {id} loaded")
            id += 1
            if id > 24:
                break
        
        except AttributeError:
            print("\nImage not loaded, check path\n")
            break

        contours = pp.pre_process(Image_i.img_scan)
        
        i_list = [Image_i.id]
        q = plot_rgb_values_of_contour(Image_i.img_scan, contours)
       
        if q is not None:    
            i_list.append(q[0])
            i_list.append(q[1])
            quartiles.append(i_list)
                    
        create_excel_file(quartiles)        

if __name__ == '__main__':
    path_to_imgs = r"C:\Users\Matheus\Desktop\NanoTechnologies_Lab\Phase A\data\pincolor_list\*"
    main(path_to_imgs)


