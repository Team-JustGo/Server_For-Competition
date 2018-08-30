from flask_restful import Resource, reqparse
from app.model.Login import *


class SocialLogin(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('userId',
                        type=str,
                        required=True,
                        help="이 인수는 비워 둘 수 없습니다.")

    def post(self):

        data = SocialLogin.parser.parse_args()

        if UserIdInDB