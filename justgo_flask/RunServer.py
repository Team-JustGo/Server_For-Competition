import os
from flask import Flask, flash, redirect, jsonify, request, url_for, send_from_directory
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_restful import Api, Resource

from app_N.resources.Login import SocialLogin
from app_N.resources.main import UserMain
from app_N.resources.ProfileImage import ChangeProfileImage
from app_N.resources.ProfileName import ChangeProfileName
from app_N.resources.TourSpot import TourSpot
from app_N.resources.ProfileInfo import ProfileInfo
from app_N.resources import connect

UPLOAD_FOLDER = './FileHAM'

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "INEEDMORESPEED"
app.config['SECRET_KEY'] = "ASDFGH"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 저장 가능한 파일의 최대 크기 = 16MiB
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.config['JSON_AS_ASCII'] = False

jwt = JWTManager(app)
api = Api(app)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


api.add_resource(SocialLogin, '/api/user/login')
api.add_resource(UserMain, '/api/user/main')
api.add_resource(ChangeProfileImage, '/api/user/profile-image')
api.add_resource(ChangeProfileName, '/api/user/profile-name')
api.add_resource(TourSpot, '/api/user/tour-spot')
api.add_resource(ProfileInfo, '/api/user/profile')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=7777)
