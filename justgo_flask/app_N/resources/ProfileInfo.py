# -*-coding: utf-8

import json
from flask import Response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app_N.resources import connect
from functools import wraps


def as_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = f(*args, **kwargs)
        res = json.dumps(res, ensure_ascii=False).encode('utf8')
        return Response(res, content_type='application/json; charset=utf-8')
    return decorated_function()


class ProfileInfo(Resource):

    @as_json
    @jwt_required
    def get(self):
        id_token = get_jwt_identity()
        user_list = connect.db.user.find_one({"userId": id_token})

        if user_list:
            all_var = \
                list(connect.db.user.find({"userId": "by09115"}, {"profileImage": 1, "profileName": 1, "_id": 0}))[0]
            userName = all_var.get('profileName')
            userImage = all_var.get('profileImage')
            return {

            }

        elif not user_list:
            return {"result": "Invalid JWT or ID hasn't signed up."}
