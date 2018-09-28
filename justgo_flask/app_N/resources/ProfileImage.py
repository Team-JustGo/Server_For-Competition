import werkzeug
from flask_restful import Resource, reqparse
from app_N.resources import connect
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.utils import secure_filename
import os


class ChangeProfileImage(Resource):
    user = connect.user

    @jwt_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('profile-image', type=werkzeug.FileStorage, required=True, location='files')
        _parsed = parser.parse_args()
        _profile_image = _parsed['profile-image']
        # temp = '/home/ubuntu/Server_For-Competition_Jaehoon/Server_For-Competition/justgo_flask/FileHAM' + _profile_image.filename

        filename = secure_filename(_profile_image.filename)
        connect.saveinfo(_profile_image, filename)
        image_url = connect.ImageUrl(filename)
        token_to_user = get_jwt_identity()
        user_id_in_lists = connect.db.user.find_one({"userId": token_to_user})

        if user_id_in_lists:

            before_file = list(connect.db.user.find({"userId": token_to_user}, {"profileImage": 1, "_id": 0}))[0].get('profileImage')
            before_file_root = '/home/ubuntu/Server_For-Competition_Jaehoon/Server_For-Competition/justgo_flask/FileHAM' + before_file[8:]

            if os.path.isfile(before_file_root):
                os.remove(before_file_root)

            connect.db.user.update({"userId": token_to_user}, {"$set": {"profileImage": image_url}})
            return {"result": "Success",
                    "uri": image_url}, 205  # return the status code 205 and "Success"

        elif not user_id_in_lists:
            return {"result": "Failure"}, 404  # OTL... It was failed...
