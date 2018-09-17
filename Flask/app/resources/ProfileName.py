from flask_restful import Resource
from pymongo
from resources import connect
from flask_jwt_extended import jwt_required, get_jwt_identity


class ChangeProfileName(Resource):
    user = connect.user

    @jwt_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        _parsed = parser.parse_args()
        _profile_name = _parsed['name']
        follow_jwt = get_jwt_identity()
        token_for_userId = connect.db.user.find_one({"userId": follow_jwt})

        if token_for_userId:
            connect.db.user.update({"userId": follow_jwt}, { $set: {"name": _profile_name}})
            return {"result": "Success"}, 205

        elif not token_for_userId:
            return {"result": "Failure"}, 404