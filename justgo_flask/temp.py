from app_N.resources import connect
import os

# connect.db.user.insert_one({"profileName": "관리자1"}, {"$set": {"profileImage": "uploads/common-image.jpg"}})

connect.db.user.update({"userId": "test001"}, {"$set": {"profileImage": "uploads/common-image.jpg"}})

etcvar = list(connect.db.user.find({"userId": "by09115"}, {"profileImage": 1, "_id": 0}))[0].get('profileImage')[8:]

print(etcvar)

connect.db.user.update({"userId": "by09115"}, {"$set": {"wentspot": [{"tourId": "문화마을아파트"}]}})