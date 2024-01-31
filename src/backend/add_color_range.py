from connect_to_db import connect_to_mongo

def add_color_range_to_db():
    
    client = connect_to_mongo()
    
    db = client.ampli_cv
    collection = db.color_ranges

    # Insert a document
    post = [
        {"color_name": "Red", "color#" : 1, "min" : (122,13,34), "max" : (208,145,160)},
        {"color_name": "Blue", "color#" : 2, "min" : (7,19,139), "max" : (147,148,242)},
        {"color_name": "Green", "color#" : 3, "min" : (80,117,54), "max" : (163,181,156)},
        {"color_name": "Purple", "color#" : 4, "min" : (83,36,143), "max" : (148,122,206)},
            
            ]
    post_id = collection.insert_many(post).inserted_ids
    print(post_id)

    client.close()

if __name__ == "__main__":
    add_color_range_to_db()