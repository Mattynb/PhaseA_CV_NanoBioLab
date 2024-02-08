from connect_to_db import connect_to_mongo

def identify_block(block):

    client = connect_to_mongo()
    
    db = client.ampli_cv
    collection = db.color_ranges
    
    sequence = []
    for rgb in block.raw_sequence:
        number = rgb_to_number(rgb, collection)
        sequence.append(number)

    #block_collection = db.block_types
    
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

    for number in numbers:
        print(number['color_name'])    
        print(f"r: {r}, g: {g}, b: {b}\n")

    return numbers


if __name__ == '__main__':
    ...