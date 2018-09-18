import werkzeug
from flask_restful import Resource, reqparse
from justgo_flask.app_N.resources import connect
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.utils import secure_filename
from justgo_flask import RunServer


class ChangeProfileImage(Resource):
    user = connect.user

    @jwt_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('profile-image', type=werkzeug.FileStorage(), required=True, location='files')
        _parsed = parser.parse_args()
        _profile_image = _parsed['profile-image']
        filename = secure_filename(_profile_image.filename)
        RunServer.saveinfo(_profile_image, filename)
        ImageUrl = RunServer.ImageUrl(filename)
        token_to_user = get_jwt_identity()
        userId_in_lists = connect.db.user.find_one({"userId": token_to_user})

        if userId_in_lists:
            connect.db.user.update({"name": token_to_user}, {"$set": {"profileImage": ImageUrl}})
            return {"result": "Success"}, 205

        elif not userId_in_lists:
            return {"result": "Failure"}, 404
