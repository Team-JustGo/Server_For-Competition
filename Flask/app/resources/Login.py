from flask import request, Response, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from resources import connect


class SocialLogin(Resource):

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('userId', type=str, required=True)
        parser.add_argument('name', type=str)
        parser.add_argument('picture', type=str)
        requests = parser.parse_args()
        user = connect.user
        _userId = requests['userId']
        _name = requests['name']
        _picture = requests['picture']
        access_token = create_access_token(_userId)
        success_200 = {"result": "Success",
                       "jwt": access_token}
        multi_user_id = []
        second_situation =  # DB에 회원가입 정보 저장(Input: userName, profileImage | Output:

        user_in_list = connect.db.user.find_one({"userId": _userId})

        if user_in_list:
            return success_200, 200

        elif not user_in_list and _userId and _name and _picture:
            connect.in_user.insert_one({"profileImage": _picture,
                                        "profileName": _name,
                                        "userId": _userId,
                                        "wentspot": [
                                            {
                                                "tourId": "Undefined"
                                            }
                                        ]})
            return success_200, 200

        elif not (_userId and _name and _picture):
            return {"result": "I am a teapot"}, 418
