from ..connect_to_db import connect_to_mongo

def add_color_range():

    
    client = connect_to_mongo()
    
    db = client.ampli_cv
    collection = db.color_ranges

    # Insert a document
    post = [
        {"color_name": "Red", "color#" : 1, "min": (150,0,0), "max": (255,150,87+40)},
        {"color_name": "Blue", "color#" : 2, "min": (49-40,77-40,150), "max": (104,77+40+50,255)},
        {"color_name": "Green", "color#" : 3, "min": (50,100,0), "max": (149,255,125)},
        {"color_name": "Purple", "color#" : 4, "min": (105,78-40,150), "max": (255+25,78+40+50,255)},
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
    add_color_range()