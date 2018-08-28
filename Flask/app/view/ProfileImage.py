from flask import Flask
from flask_restful import Api

app = Flask(__name__)

api = Api(app)

""" 본 파일은 유저의 프로필 이미지 변경을 위해 작성되었음.
    <여기서 잠깐!> 아직 생각 못한 것들
    1. 유저의 프로필 url은 어떻게 줄건지?
    """

class ProfileImage:
    def put(self):
