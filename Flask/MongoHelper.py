from mongoengine import *

connect('tumblelog')

class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)

class Posts(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User)

    meta = {'allow_inheritance': True}

class TextPosts(Posts):
    content = StringField()

class ImagePosts(Posts):
    image_path = StringField()

class LinkPost(Posts):
    link_url = StringField()