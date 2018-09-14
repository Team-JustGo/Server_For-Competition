from flask import Flask, jsonify, request, url_for
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_restful import Api
from resources.Login import SocialLogin
from resources.main import UserMain
import resources.connect

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "INEEDMORESPEED"
jwt = JWTManager(app)
api = Api(app)


api.add_resource(SocialLogin, '/api/user/login')
api.add_resource(UserMain, '/api/user/main')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
