from flask_restful import Resource, reqparse
from app.resources import connect


class SocialLogin(Resource):

    user = connect.user

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', type=str, required=True)
        args = parser.parse_args()
        _userId = args['userId']

