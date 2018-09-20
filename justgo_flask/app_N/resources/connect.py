import os
from pymongo import MongoClient
from flask import current_app, url_for

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

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'bmp', 'gif', 'png'])

def saveinfo(announce, filename):
    announce.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))


def ImageUrl(filename):
    return url_for('uploaded_file', filename=filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS