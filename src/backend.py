import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from secrets_ import MONGO_PASSWORD


def connect_to_mongo():
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

    # Close the connection
    client.close()



def identify_blocks(Grid):
    """
    ### Identify blocks
    ------------------
    Function that identifies the blocks of the grid and encodes them.

    #### Args:
    grid: grid object
    """

    for x in Grid.grid:
        for sq in x:
            if sq.is_block == True:
                rgbs, _ = sq.get_pins_rgb(0)

                # fixing the order from tr,tl,br,bl to clockwise starting from top-right
                for rgb in rgbs:
                    try:
                        br = rgb[2]
                        rgb[2] = rgb[3]
                        rgb[3] = br
                    except:
                        pass

                # compare each pin with the excel file to see what # color they are
                sequence = []
                for pin in rgbs:
                    # pin = [r,g,b]

                    sequence.append(identify_pin(pin))
                
                print(sequence)
            


def identify_pin(pin):
    excel = pd.read_excel(r"quartiles.xlsx")    

    for color in excel.values:
        # color = [r,g,b, color_name]

        # if the pin is the same color as the color in the excel file
        if pin[0] in range(color[1], color[4]):
            if pin[1] in range(color[2], color[5]):
                if pin[2] in range(color[3], color[6]):
                    return color[0]

if __name__ == "__main__":
    connect_to_mongo()
