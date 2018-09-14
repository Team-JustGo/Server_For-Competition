from flask_restful import reqparse, Resource
from flask import request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from resources import connect, Login


class UserMain(Resource):

    @jwt_required
    def get(self):

        user = connect.user
        current_token = get_jwt_identity()

        for i in range(user.count()):
            if current_token == list(user[i].values())[1]:
                profileUrl = list(user[i].values())[3]
                tourName = list(user[i].values())[4]
                success_response = {
                    "result": "Success",
                    "identity": current_token,
                    "profileUrl": profileUrl,
                    "reqComment": [
                        {
                            "tourName": tourName.encode('utf-8'),
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
                            "tourName": tourName.encode('utf-8'),
                            "tourImage": "Undefined"
                        }
                    ]
                }

        return success_response, 200