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
        requests = parser.parse_args()
        _userId = requests['userId']
        _name = requests['name']

        success_200 = {"result": "Success",
                       "jwt": create_access_token(_userId)}
        user_in_list = connect.db.user.find_one({"userId": _userId})


# connect.db.user.update({"name": _userId}, {"$set": {"profileImage": ImageUrl_}})

        if user_in_list:
            return success_200, 200     # Success!

        elif not user_in_list:

            if _userId and _name:      # DB에 userId가 없지만 userId와 name이 들어온 경우 - 회원가입
                connect.db.user.insert({"profileImage": "uploads/common-image.jpg",
                                        "profileName": _name,
                                        "userId": _userId,
                                        "wentspot": []})
                return success_200, 200

            return {"result": "I am a teapot"}, 418  # How wonderful!
