
def identify_blocks(Grid):
    """
    ### Identify blocks
    ------------------
    Function that identifies the type of blocks based on their sequence of pin colors.

    #### Args:
    grid: grid object
    """

    for block in Grid.blocks:
        rgbs, _ = block.get_pins_rgb(0)

        # fixing the order from tr,tl,br,bl to tl, tr, bl, br
        for rgb in rgbs:
            try:
                # swap br and bl
                br = rgb[2]
                rgb[2] = rgb[3]
                rgb[3] = br

                # swap tr and tl
                tr = rgb[0]
                rgb[0] = rgb[1]
                rgb[1] = tr

            except:
                pass

        # compare each pin with the excel file to see what # color they are
        sequence = []
        for pin in rgbs:
            # pin = [r,g,b]

            sequence.append(identify_pin(pin))
        
        print(sequence)



