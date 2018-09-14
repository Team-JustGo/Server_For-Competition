from flask import request, Response, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from resources import connect


class SocialLogin(Resource):


    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('userId',type=str,required=True)
        parser.add_argument('name',type=str)
        parser.add_argument('picture',type=str)
        requests = parser.parse_args()
        user = connect.user
        _userId = requests('userId', None)
        _name = requests['name']
        _picture = requests['picture']
        access_token = create_access_token(_userId)
        success_200 = {"result": "Success",
                       "jwt": access_token}
        multi_user_id = []
        second_situation = {"profileImage": _picture,
                            "profileName": _name,
                            "userId": _userId,
                            "wentspot": [
                                {
                                    "tourId": "Undefined"
                                }
                            ]}     # DB에 회원가입 정보 저장(Input: userName, profileImage | Output:

        for i in range(user.count()):
            multi_user_id.append(list(user[i].values())[1])

        print(multi_user_id)

        for j in range(user.count()):
            if _userId in multi_user_id:
                get_jwt_identity(access_token)
                return success_200, 200

            if (_userId not in multi_user_id) and _userId and _name and _picture:
                connect.in_user.insert_one(second_situation)
                return success_200, 200

            if (_userId not in multi_user_id) and _userId == None and _name == None and _picture == None:
                return {"result": "I am a teapot"}, 418



