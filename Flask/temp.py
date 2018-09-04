from pymongo import MongoClient
import os
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse

ID = {"by09115", "yej9569"}

connection_set = {
    'user': 'by09115',
    'password': 'hunter5402'
}

uri = "mongodb://{user}:{password}@ds018508.mlab.com:18508/justgo".format(**connection_set)
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

"""
print(collection_user, '\n',  user, '\n', list(user[0].values())[1])
print(user.count())
for i in range(user.count()):
    print(list(user[i].values())[1])


for i in range(user.count()):
    if 'by09115' in list(user[i].values())[1]:
        print("Success")
"""

print(list(user[0].values()))