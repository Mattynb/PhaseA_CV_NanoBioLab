from connect_to_db import connect_to_mongo

def add_color_range_to_db():
    
    client = connect_to_mongo()
    
    db = client.ampli_cv
    collection = db.color_ranges

    # Insert a document
    """post = [
        {"color_name": "Red", "color#" : 1, "min" : (122,13,34), "max" : (208,145,160)},
        {"color_name": "Blue", "color#" : 2, , "col"min" : (7,19,139), "max" : (147,148,242)},
        {"color_name": "Green", "color#" : 3, "min" : (80,117,54), "max" : (163,181,156)},
        {"color_name": "Purple"or#" : 4, "min" : (83,36,143), "max" : (148,122,206)},    
        ]"""

    post = [
        {"color_name": "Red", "color#" : 1, "min" : (209-40,88-40,87-40), "max" : (255,88+40,87+40)},
        {"color_name": "Blue", "color#" : 2, "min" : (49-40,77-40,232-40), "max" : (49+40,77+40,255)},
        {"color_name": "Green", "color#" : 3, "min" : (135-40,191-40,110-40), "max" : (135+40, 255,110+40)},
        {"color_name": "Purple", "color#" : 4, "min" : (140-40,78-40,224-40), "max" :  (140+40,78+40,224+40)},
    ]

    post_id = collection.insert_many(post).inserted_ids
    print(post_id)

    client.close()

def delete_all():
    client = connect_to_mongo()
    
    db = client.ampli_cv
    collection = db.color_ranges

    collection.delete_many({})

    client.close()

if __name__ == "__main__":
    delete_all()
    add_color_range_to_db()