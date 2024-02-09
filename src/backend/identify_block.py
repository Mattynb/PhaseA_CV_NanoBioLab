from .connect_to_db import connect_to_mongo
from itertools import permutations, combinations

def identify_block(block):

    client = connect_to_mongo()
    
    db = client.ampli_cv
    collection = db.color_ranges
    
    sequence = []
    seq_2 = []
    for rgb in block.raw_sequence:
        seq_2.append(rgb)
        number = rgb_to_number(rgb, collection)
        sequence.append(number)

    #print(f'RGB sequence: {seq_2}')
    print(f'# sequence: {sequence}')
    
    block_collection = db.block_types
    
    """This is bad"""
    for perm in permutations(sequence, len(sequence)):
        query = {
            'Sequence': list(perm)
        }
        block_type = block_collection.find_one(query)
        if block_type:
            print(f'Block: {block_type["block_name"]}\n')
            client.close()
            return

    print('No block with this sequence\n')

    
    client.close()


def rgb_to_number(rgb, collection):
    r, g, b = rgb
    
    query = {
        'min.0': {'$lte': r},  # Compare Red
        'max.0': {'$gte': r},  
        'min.1': {'$lte': g},  # Compare Green
        'max.1': {'$gte': g},  
        'min.2': {'$lte': b},  # Compare Blue
        'max.2': {'$gte': b}, 
    }

    numbers = collection.find(query)

    if numbers.count() == 0:
        #print(f"No color found for r: {r}, g: {g}, b: {b}\n")
        return None
    
    if numbers.count() == 1:
        for number in numbers:
            return number['color#']
    
    for number in numbers:
        print (number['color#'])

    


if __name__ == '__main__':
    ...