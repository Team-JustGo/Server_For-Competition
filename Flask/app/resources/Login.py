from flask import request, Response, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from resources import connect


class SocialLogin(Resource):


    def post(self):
        user = connect.user
        payload = request.json
        _userId = payload['userId']
        _name = payload['name']
        _picture = payload['picture']
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
                return success_200, 200

            if (_userId not in multi_user_id) and _userId and _name and _picture:
                connect.in_user.insert_one(second_situation)
                return {"result": "Success"}, 200

            if (_userId not in multi_user_id) and _userId == None and _name == None and _picture == None:
                return {"result": "I am a teapot"}, 418



