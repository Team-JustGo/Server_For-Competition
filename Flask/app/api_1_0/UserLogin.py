from flask import Flask, request, jsonify

from app.api_1_0.models.user import User

app = Flask(__name__)


# def get_users_url():


class UserLogin():

    def post(self):

        request_data = request.get_json()
        user = User(userId=request_data('userId'))

        outValue = {
            'result': 'success',
            'profileUrl': get_users_url(),

        }
        return jsonify(outValue)