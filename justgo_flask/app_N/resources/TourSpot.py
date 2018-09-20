from flask_restful import Resource, reqparse
from app_N.resources import connect
from flask_jwt_extended import get_jwt_identity, jwt_required

class TourSpot(Resource):

    @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('tourId', type=str, required=True)
        payload = parser.parse_args()
        _tourId = payload['tourId']
        get_userId_in_token = get_jwt_identity()
        db_in_userId = connect.db.user.find_one({"userId": get_userId_in_token})

        if db_in_userId:
            connect.db.user.update({"userId": get_userId_in_token}, {"$push": {"wentspot": { "tourId": _tourId }}})
            return {"result": "Success"}, 205

        elif not db_in_userId:
            return {"result": "Failure"}, 404