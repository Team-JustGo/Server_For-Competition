from flask_restful import reqparse, Resource
from flask import request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from resources import connect, Login


class UserMain(Resource):

    def get(self):

        user = connect.user
        payload = request.json
        _X_TOKEN = payload['X-Access-Token']


        for i in range(user.count()):
            profileUrl = list(user[i].values())[3]
            tourName = list(SocialLogin.user[i].values())[4]

        success_response = {
            "result": "Success",
            "profileUrl": list(user[i].values())[3],
            "reqComment": [
                {
                    "tourName": "Undefined",
                    "tourImage": "Undefined"
                }
            ],
            "recommendSpot": [
                {
                    "reqTime": 500,
                    "Theme": "Undefined"
                }
            ],
            "reqShare": [
                {
                    "tourName": list(SocialLogin.user[i].values())[4],
                    "tourImage": "Undefined"
                }
            ]
        }
        return success_response, 200