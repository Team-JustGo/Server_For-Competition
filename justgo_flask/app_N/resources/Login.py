import werkzeug
from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse
from app_N.resources import connect
from werkzeug.utils import secure_filename


class SocialLogin(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', type=str, required=True)
        parser.add_argument('name', type=str)
        parser.add_argument('picture', type=werkzeug.FileStorage, location='files')
        requests = parser.parse_args()
        _userId = requests['userId']
        _name = requests['name']
        _picture = requests['picture']
        if _picture:
            filename = secure_filename(_picture.filename)
            connect.saveinfo(_picture, filename)
            ImageUrl_ = connect.ImageUrl(filename)
        elif not _picture:
            ImageUrl_ = None

        success_200 = {"result": "Success",
                       "jwt": create_access_token(_userId),
                       "image-url": ImageUrl_}
        user_in_list = connect.db.user.find_one({"userId": _userId})

        if user_in_list:
            if _picture:
                connect.db.user.update({"name": _userId}, {"$set": {"profileImage": ImageUrl_}})
            return success_200, 200

        elif not user_in_list and _userId and _name and _picture:
            connect.in_user.insert({"profileImage": _picture,
                                    "profileName": _name,
                                    "userId": ImageUrl_,
                                    "wentspot": [
                                        {
                                            "tourId": "Undefined"
                                        }
                                    ]})
            return success_200, 200

        elif not (_userId and _name and _picture):
            return {"result": "I am a teapot"}, 418
