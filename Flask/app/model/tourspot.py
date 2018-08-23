from datetime import datetime

from mongoengine import *


class TourSpot(document):
    tourId = StringField(required=True)
    userId = StringField(required=True)
    date = DateTimeField(required=True)
    rate = StringField(required=True)
    content = StringField(required=True)

    comment = [{"userId", "date", "rate", "content"}]
