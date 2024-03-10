from .connect_to_db import connect_to_mongo

def identify_block(block):

    # Open connection to MongoDB
    client = connect_to_mongo()
    
    # Connect to the color_ranges database collection
    db = client.ampli_cv
    collection = db.color_ranges
    
    
    # Get the RGB sequence of the 
    # block in rgb and numerical form
    sequence_rgb = []
    sequence_numerical = []
    for rgb in block.raw_sequence:
        sequence_rgb.append(rgb)

        number = rgb_to_number(rgb, collection)
        sequence_numerical.append(number)

    print(f'RGB sequence: {sequence_rgb}')
    print(f'Numerical sequence: {sequence_numerical}')
    

    # Connect to the block_types collection
    block_collection = db.block_types
    
    # Check if the sequence is in the database
    # If it is, print the block type
    for _ in range(len(sequence_numerical)):
        # Rotate the sequence
        sequence_numerical = sequence_numerical[1:] + sequence_numerical[:1]
        
        # Look for the sequence in the database
        query = {'Sequence': sequence_numerical}
        
        # If the sequence is found, print the block type and return
        block_type = block_collection.find_one(query)
        if block_type:
            print(f'Block: {block_type["block_name"]} at {block.index}\n')
            client.close()
            return
        
    # If the sequence is not found, print unknown
    print(f'Block: Unknown at {block.index}\n')
    client.close()


def rgb_to_number(rgb, collection):
    """ 
    Convert an RGB value to a number using the color_ranges collection in the database.
    """
    r, g, b = rgb
    
    query = {
        'min.0': {'$lte': r},  # Compare Red range
        'max.0': {'$gte': r},  
        'min.1': {'$lte': g},  # Compare Green range
        'max.1': {'$gte': g},  
        'min.2': {'$lte': b},  # Compare Blue range
        'max.2': {'$gte': b}, 
    }

    numbers = collection.find(query)

    for number in numbers:
        return number['color#']
    
    print(f"Multiple colors found for r: {r}, g: {g}, b: {b}\n")
    for number in numbers:
        print(number['color#'])
    for number in numbers:
        return number['color#']



if __name__ == '__main__':
    ...