from image import Image
from image import image_loader, pre_process as pp
import numpy as np
import cv2 as cv
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
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
    df = pd.DataFrame(quartiles, columns=['id', 'Low_R', 'Low_G', 'Low_B', 'High_R', 'High_G', 'High_B'])

    # Save the DataFrame to an Excel file
    df.to_excel('quartiles.xlsx', index=False)

def plot_quartiles_3d(thresh):
    """
    ### Plot Quartiles in 3D (RGB)
    Plots the quartile values in a 3D scatter plot.

    #### Args:
    quartiles: list of lists containing quartiles values
    """
    high = []
    low = []
    i = 0
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for quartiles in thresh:
        # Extract RGB values from quartiles
        r = [q[0] for q in quartiles]
        g = [q[1] for q in quartiles]
        b = [q[2] for q in quartiles]

        if i == 0:
            low = [r, g, b]
        if i == 1:
            high = [r, g, b]

        # Create a 3D scatter plot
        ax.scatter(r, g, b, label='thresholds')
        
        i += 1


    # low  = [[r...], [g...], [b...]] 
    # high = [[r...], [g...], [b...]] 
    # Connect the high and low threshold points with a line

    # ...

    # Connect the high and low threshold points with a line
    for i in range(len(low[0])):
        # Calculate the overlap between cubes
        overlap_low = [max(low[0][1], low[0][2]), max(low[1][0], low[1][2]), max(low[2][1], low[2][2])]
        overlap_high = [min(high[0][1], high[0][2]), min(high[1][0], high[1][2]), min(high[2][0], high[2][1])]

        # Check if there is overlap between cubes
        if overlap_low[0] < overlap_high[0] and overlap_low[1] < overlap_high[1] and overlap_low[2] < overlap_high[2]:
            ax.plot([low[0][i], high[0][i]], [low[1][i], high[1][i]], [low[2][i], high[2][i]], color='black')

            # Draw the overlapping cube
            cube = [
                [overlap_low[0], overlap_low[0], overlap_high[0], overlap_high[0], overlap_low[0], overlap_low[0], overlap_high[0], overlap_high[0]],
                [overlap_low[1], overlap_high[1], overlap_high[1], overlap_low[1], overlap_low[1], overlap_high[1], overlap_high[1], overlap_low[1]],
                [overlap_low[2], overlap_low[2], overlap_low[2], overlap_low[2], overlap_high[2], overlap_high[2], overlap_high[2], overlap_high[2]]
            ]
            cube_collection = Poly3DCollection([list(zip(cube[0], cube[1], cube[2]))], alpha=0.25, linewidths=1, edgecolors='r')
            ax.add_collection3d(cube_collection)
            
    # Set labels and title
    ax.set_xlabel('Red')
    ax.set_ylabel('Green')
    ax.set_zlabel('Blue')
    ax.set_title('Thresholds in 3D (RGB)')
    ax.legend()

    # Show the plot
    plt.show()


def main(path_to_imgs):
    """
    ### Main function
    Loads all the images in a folder and creates an Image object for each image.

    #### Args:
    path_to_imgs: path to image folder
    """

    # loading images
    images_og = image_loader(path_to_imgs)

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
            i_list.append(round(q[0][2]))
            i_list.append(round(q[0][1]))
            i_list.append(round(q[0][0]))
            i_list.append(round(q[1][2]))
            i_list.append(round(q[1][1]))
            i_list.append(round(q[1][0]))
            quartiles.append(i_list)
    
    low = [thresh[:3] for thresh in [q[1:] for q in quartiles]] 
    high = [thresh[2:] for thresh in [q[1:] for q in quartiles]]

    print(low)

    low = [[100, 100, 100], [110, 110, 110]]
    high = [[200, 200, 200], [210, 210, 210]]

   
    plot_quartiles_3d([low,high])
    #create_excel_file(quartiles)        

if __name__ == '__main__':
    path_to_imgs = r"C:\Users\Matheus\Desktop\NanoTechnologies_Lab\Phase A\data\pincolor_list\*"
    main(path_to_imgs)

    print("get the one drive pictire and test to see if block a and b works")



