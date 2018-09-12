from flask_restful import reqparse, Resource
from app.resources import connect, Login


class UserMain(Resource):

    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('X-Access-Token', type=str, required=True)
        args = parser.parse_args()
        _Token = args['X-Access-Token']

        user = connect.user

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