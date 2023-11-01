from obj.image import Image_loader

from finders.edge_finder import EdgeFinder
from finders.circle_finder import CircleFinder
from finders.pin_finder import PinFinder


class PhaseA:
    def __init__(self, img_dir, ):
        self.images = Image_loader(img_dir)

        self.main()

    def main(self):
        # pre_process images: angle_fix -> isolate_foreground -> resize_2_std
        for img in self.images:
            img.pre_process(0)

            
        # start finding 
        for img in self.images:
            img.edges = EdgeFinder(img)
            img.circles = CircleFinder(img)
            img.blocks = PinFinder(img)
            for block in img.blocks:
                block.encoding_finder()



        







            




