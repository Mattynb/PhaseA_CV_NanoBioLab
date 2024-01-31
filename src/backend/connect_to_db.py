from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from secrets_ import MONGO_PASSWORD



def connect_to_mongo():
    """
    Connect to MongoDB Atlas and return the client object.
    """
    
    atlas_connection_uri = f"mongodb+srv://matheusberbet001:{MONGO_PASSWORD}@amplicluster.0k26okc.mongodb.net/?retryWrites=true&w=majority"

    # Connect to your Atlas cluster
    client = MongoClient(atlas_connection_uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    # Specify the database and collection
    #db = client.test
    #collection = db.test_collection

    # Insert a document
    #post = {"author": "John", "text": "My first blog post!"}
    #post_id = collection.insert_one(post).inserted_id
    #print(post_id)

    return client


if __name__ == "__main__":
    connect_to_mongo()