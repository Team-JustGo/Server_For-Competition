from flask import Flask
from flask_restful import Api
from pymongo import MongoClient

uri = "mongodb://by09115:hunter5402@ds018508.mlab.com:18508/justgo"

client = MongoClient(uri)
db = client["justgo"]

collection_contact = db.contact
contact = collection_contact.find()

collection_tourspot = db.tourspot
tourspot = collection_tourspot.find()

collection_user = db.user
user = collection_user.find()

app = Flask(__name__)
api = Api(app)

myID = "by0129115"
TMI = db.user.find_one({"userId": myID})

if not TMI:
    print("아몰라")
