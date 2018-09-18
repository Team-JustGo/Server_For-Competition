from flask import Flask, flash, redirect, jsonify, request, url_for, send_from_directory
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_restful import Api, Resource
from resources.Login import SocialLogin
from resources.main import UserMain
from resources.ProfileImage import ChangeProfileImage
from resources.ProfileName import ChangeProfileName
from resources.Upload import UploadImages
from resources import connect

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "INEEDMORESPEED"
app.config['SECRET_KEY'] = UploadImages.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 저장 가능한 파일의 최대 크기 = 16MiB

jwt = JWTManager(app)
api = Api(app)


@app.route('/')
def helloworld():
    return "<h1>Welcome to Just-go&#39;s second API Server!</h1><p>This API will give you many data! It so fun!</p><p>~~[This page is TEST]</p>"


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


api.add_resource(SocialLogin, '/api/user/login')
api.add_resource(UserMain, '/api/user/main')
api.add_resource(ChangeProfileImage, '/api/user/profile-image')
api.add_resource(ChangeProfileName, '/api/user/profile-name')
api.add_resource(UploadImages, '/uploads')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=7777)
