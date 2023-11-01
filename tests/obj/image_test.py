from cv2 import imshow, waitKey, destroyAllWindows

def Image_load_test(Image_loader: function):
    
    Images = Image_loader(r"C:\Users\Matheus\Desktop\NanoTechnologies_Lab\Phase A\data\img") 
    for i in Images:
        imshow(str(i.id), i.img_og)
    waitKey(0)
    destroyAllWindows()

def Image_resize_test(Image_loader: function):
    # Image_loader test
    from cv2 import imshow, waitKey, destroyAllWindows
    Images = Image_loader(r"C:\Users\Matheus\Desktop\NanoTechnologies_Lab\Phase A\data\img") 
    for i in Images:
        i.resize_2_std()
        imshow(str(i.id), i.img_std_size)
    waitKey(0)
    destroyAllWindows()