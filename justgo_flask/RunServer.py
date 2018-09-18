import os
from flask import Flask, flash, redirect, jsonify, request, url_for, send_from_directory
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_restful import Api, Resource

from justgo_flask.app_N.resources.Login import SocialLogin
from justgo_flask.app_N.resources.main import UserMain
from justgo_flask.app_N.resources.ProfileImage import ChangeProfileImage
from justgo_flask.app_N.resources.ProfileName import ChangeProfileName
from justgo_flask.app_N.resources import connect

UPLOAD_FOLDER = './FileHAM'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'bmp', 'gif', 'png'])

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "INEEDMORESPEED"
app.config['SECRET_KEY'] = "ASDFGH"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 저장 가능한 파일의 최대 크기 = 16MiB

jwt = JWTManager(app)
api = Api(app)

def saveinfo(announce, filename):
    announce.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

def ImageUrl(filename):
    url_for('uploaded_file', filename=filename)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


api.add_resource(SocialLogin, '/api/user/login')
api.add_resource(UserMain, '/api/user/main')
api.add_resource(ChangeProfileImage, '/api/user/profile-image')
api.add_resource(ChangeProfileName, '/api/user/profile-name')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=7777)
