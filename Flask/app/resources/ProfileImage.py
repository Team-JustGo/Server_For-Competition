from flask_restful import Resource, reqparse
from resources import connect
from pymongo
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

        for i in range(ChangeProfileImage.user.count()):
            if list(ChangeProfileImage.user[i].values())[1] == token_to_user:
                connect.in_user.update({ "name": token_to_user }, { $set: { "profileImage": _profile_image} })
                return {"result": "Success"}, 205


