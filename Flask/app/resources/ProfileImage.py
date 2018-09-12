from flask_restful import Resource, reqparse
from app.resources import connect


class ChangeProfileImage(Resource):
    user = connect.user

    def get(self):
        return