from flask import Flask, jsonify
from flask_restful import Api
from app.resources.Login import SocialLogin
import app.resources.connect

app = Flask(__name__)
app.secret_key = 'jaehoonjaehoon123'
api = Api(app)

api.add_resource(SocialLogin, '/api/user/login')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
