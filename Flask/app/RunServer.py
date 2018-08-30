from flask import Flask
from flask_restful import Api
from flask_jwt import JWT


from app.resources.Login import SocialLogin


app = Flask(__name__)
api = Api(app)

api.add_resource(SocialLogin, '/api/user/login')