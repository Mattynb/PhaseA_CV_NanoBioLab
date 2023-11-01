
def Image_load_test(Image_loader: function):
    from obj.image import Image_loader
    from cv2 import imshow, waitKey, destroyAllWindows
    Images = Image_loader(r"C:\Users\Matheus\Desktop\NanoTechnologies_Lab\Phase A\data\img") 
    for i in Images:
        imshow(str(i.id), i.img_og)
        waitKey(0)
        destroyAllWindows()

