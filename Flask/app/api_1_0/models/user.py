from mongoengine import *


class User(Document):
    tourId = StringField(required=True)
    userId = StringField(required=True)
    profileName = StringField(required=True)
    profileImage = StringField(required=True)
    wentSpot = [{'tourId'}]
