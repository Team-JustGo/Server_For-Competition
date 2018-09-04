from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

"""
'user': os.environ['DBUSERID']
'password': os.environ['PASSWORD']
"""

connection_set = {
    'user': 'admin',
    'password': 'justgo1234'
}

uri = "mongodb://{user}:{password}@ds018508.mlab.com:18508/justgo".format(**connection_set)
db = MongoClient(uri)["justgo"]
user = db.user.find()


class SocialLogin(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', type=str, required=True)
        args = parser.parse_args()
        _userId = args['userId']

        for i in range(user.count()):
            if _userId in (list(user[i].values())[1]):
                success_response = {
                    "result": "Success",
                    "profileUrl": list(user[i].values())[3],
                    "reqComment": [
                        {
                            "tourName": "Undefined",
                            "tourImage": "Undefined"
                        }
                    ],
                    "recommendSpot": [
                        {
                            "reqTime": 500,
                            "Theme": "Undefined"
                        }
                    ],
                    "reqShare": [
                        {
                            "tourName": list(user[i].values())[4],
                            "tourImage": "Undefined"
                        }
                    ]
                }
                return jsonify(success_response), 200
            return jsonify({"result": "failed"}), 100


api.add_resource(SocialLogin, '/api/user/login')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
