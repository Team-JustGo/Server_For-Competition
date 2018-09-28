# -*-coding: utf-8

import json
from flask import Response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app_N.resources import connect


class ProfileInfo(Resource):

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
                "profileName": userName,
                "profileImage": userImage
            }

        elif not user_list:
            return {"result": "Invalid JWT or ID hasn't signed up."}
