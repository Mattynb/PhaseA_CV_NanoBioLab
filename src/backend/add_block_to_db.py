from connect_to_db import connect_to_mongo

# This function adds a block to the database whenever theres a new block type
def add_block_to_db():

    client = connect_to_mongo()
    
    db = client.ampli_cv
    collection = db.block_types

    # Insert a document
    post = {"block_name": "Wick Block", "Sequence": (1,1,1,3)}  # Sequence is tl, tr, bl, br
    post_id = collection.insert_one(post).inserted_id
    print(post_id)
    post = {"block_name": "Sample Block", "Sequence": (2,2,1,3)}
    post_id = collection.insert_one(post).inserted_id
    print(post_id)
    post = {"block_name": "Conjugate Pad", "Sequence": (3,3,3,1)}
    post_id = collection.insert_one(post).inserted_id
    print(post_id)
    post = {"block_name": "Test Block", "Sequence": (2,2,2,1)}
    post_id = collection.insert_one(post).inserted_id
    print(post_id)

    client.close()

def delete_all():
    client = connect_to_mongo()
    
    db = client.ampli_cv
    collection = db.block_types

    collection.delete_many({})

    client.close()

if __name__ == "__main__":
    delete_all()
    add_block_to_db()