from datetime import datetime

from mongoengine import *


class Contact(Document):
    """
    문의를 넣고 싶을 때를 위한 콜렉션
    """
    name = StringField(required=True)
    email = StringField(required=True)
    phone = StringField(required=True)
    content = StringField(required=True)