from pymongo import MongoClient
import os

connection_set = {
    'user': os.environ['DBUserID'],
    'password': os.environ['password']
}

uri = "mongodb://{user}:{password}@ds018508.mlab.com:18508/justgo".format(**connection_set)
client = MongoClient(uri)

