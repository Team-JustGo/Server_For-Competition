from flask import Flask, request, jsonify
from flask_restful import Api

from app.model import user

app = Flask(__name__)
api = Api(app)

"""
[구현해야 할 내용들]
처음 로그인시 고유값 얻어서 DB에 저장하기, 이미 로그인 한 유저일 시 유저 구별하기, 메인페이지 유저 정보 주기
 
"""


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