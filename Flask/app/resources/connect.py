from pymongo import MongoClient
import os


class ConnectDatabase():
    connection_set = {
        'user': os.environ['DBUserID'],
        'password': os.environ['password']
    }

    global uri
    uri = "mongodb://{user}:{password}@ds018508.mlab.com:18508/justgo".format(**connection_set)

    def connectDB(self):
        global client
        client = MongoClient(uri)

    db = client["justgo"]

    collection_contact = db.contact
    contact = collection_contact.find()

    collection_tourspot = db.tourspot
    tourspot = collection_tourspot.find()

    collection_user = db.user
    user = collection_user.find()