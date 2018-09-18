import os
from flask import Flask, flash, request, redirect, redirect, url_for, send_from_directory
from flask_restful import Resource
from werkzeug.utils import secure_filename

class UploadImages(Resource):
    UPLOAD_FOLDER = './FileHAM'
    ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'bmp', 'gif', 'png'])

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rssplit('.', 1)[1].lower() in UploadImages.ALLOWED_EXTENSIONS

    def POST(self):
        file = request.files['file']
        if file and UploadImages.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(Flask.app.config['UPLOAD_FOLDER'], filename))
            go_link = url_for('uploaded_file', filename=filename)
            return go_link

        return "COMMON_IMAGES_SERVER"