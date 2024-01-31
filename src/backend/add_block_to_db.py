from connect_to_db import connect_to_mongo

def add_block_to_db():

    client = connect_to_mongo()
    
    
    db = client.ampli_cv
    collection = db.block_types

    # Insert a document
    post = {"block_name": "Wick Block", "Sequence": (1,1,1,3)}  # Sequence is tl, tr, bl, br
    post_id = collection.insert_one(post).inserted_id
    print(post_id)

    client.close()

if __name__ == "__main__":
    add_block_to_db()

    