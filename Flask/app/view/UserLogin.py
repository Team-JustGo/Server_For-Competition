from flask import Flask, request, jsonify
from flask_restful import Api

from app.model import user

app = Flask(__name__)
api = Api(app)


class GetData:

    def get_users_url(self):
        pass

    def get_tour_name(self):
        pass

    def get_tour_image(self):
        pass

    def get_req_time(self):
        pass

    def get_theme(self):
        pass


class UserLogin:

    def post(self):
        request_data = request.get_json()
        user = User(userId=request_data('userId'))
        user.save()

        if request_data('userId') is None:

            out_value = {
                'result': 'failure',
                'profileUrl': GetData.get_users_url(),
                'reqComment': {
                    'tourName': GetData.get_tour_name(),
                    'tourImage': GetData.get_tour_image()
                },
                'recommendSpot': {
                    'reqTime': GetData.get_req_time(),
                    'theme': GetData.get_theme()
                },
                'reqShare': {
                    'tourName': GetData.get_tour_name()
                }

            }

            return jsonify(out_value), 500

        else:

            out_value = {
                'result': 'success',
                'profileUrl': GetData.get_users_url(),
                'reqComment': {
                    'tourName': GetData.get_tour_name(),
                    'tourImage': GetData.get_tour_image()
                },
                'recommendSpot': {
                    'reqTime': GetData.get_req_time(),
                    'theme': GetData.get_theme()
                },
                'reqShare': {
                    'tourName': GetData.get_tour_name()
                }
            }
            return jsonify(out_value), 200


Api.add_resource(UserLogin, '/api/user/login')