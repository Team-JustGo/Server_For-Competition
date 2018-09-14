from pymongo import MongoClient

connection_set = {
    'user': 'admin',
    'password': 'justgo1234'
}

uri = "mongodb://{user}:{password}@ds018508.mlab.com:18508/justgo".format(**connection_set)
db = MongoClient(uri)["justgo"]
in_user = db.user

user = db.user.find()

contact = db.contact.find()

tourspot = db.tourspot.find()