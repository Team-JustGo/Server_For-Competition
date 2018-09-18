from flask_restful import Resource, reqparse
from resources import connect
from flask_jwt_extended import get_jwt_identity, jwt_required


class ChangeProfileImage(Resource):
    user = connect.user

    @jwt_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('profile-image', type=str, required=True)
        _parsed = parser.parse_args()
        _profile_image = _parsed['profile-image']
        token_to_user = get_jwt_identity()
        userId_in_lists = connect.db.user.find_one({"userId": token_to_user})

        if userId_in_lists:
            connect.db.user.update({"name": token_to_user}, {"$set": {"profileImage": _profile_image}})
            return {"result": "Success"}, 205

        elif not userId_in_lists:
            return {"result": "Failure"}, 404
