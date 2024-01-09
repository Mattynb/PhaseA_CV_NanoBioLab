import pandas as pd

def identify_blocks(Grid):
    """
    ### Identify blocks
    ------------------
    Function that identifies the blocks of the grid and encodes them.

    #### Args:
    grid: grid object
    """

    for x in Grid.grid:
        for sq in x:
            if sq.is_block == True:
                rgbs, _ = sq.get_pins_rgb(0)

                # fixing the order from tr,tl,br,bl to clockwise starting from top-right
                for rgb in rgbs:
                    try:
                        br = rgb[2]
                        rgb[2] = rgb[3]
                        rgb[3] = br
                    except:
                        pass

                # compare each pin with the excel file to see what # color they are
                sequence = []
                for pin in rgbs:
                    # pin = [r,g,b]

                    sequence.append(identify_pin(pin))
                
                print(sequence)
            


def identify_pin(pin):
    excel = pd.read_excel(r"quartiles.xlsx")    

    for color in excel.values:
        # color = [r,g,b, color_name]

        # if the pin is the same color as the color in the excel file
        if pin[0] in range(color[1], color[4]):
            if pin[1] in range(color[2], color[5]):
                if pin[2] in range(color[3], color[6]):
                    return color[0]
