import os
from flask import request, send_from_directory, g
from flask_restplus import Namespace, Resource, fields
from werkzeug.utils import secure_filename

from ..models import db
from ..models.user import User
from ..helpers.authorization import Authorization
from ..config import upload_folder, allowed_extensions

ns = Namespace('uploads', description='Handle all upload related operations')


def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed_extensions


@ns.route('/', endpoint='file_endpoint')
class UploadListFiles(Resource):
    @Authorization.authorize_user
    def post(self):
        if 'file' not in request.files:
            return {'status': 'fail', 'message': 'No file uploaded.'}

        file = request.files['file']

        if file.filename == '':
            return {'status': 'fail', 'message': 'Name the file.'}

        if file and allowed_files(file.filename):
            # get the current user to update the profile_img
            user = User.query.get(g.user['user_id'])
            filename = secure_filename(file.filename).lower()
            user.profile_img = f'/api/v1/uploads/{filename}'
            db.session.commit()
            file.save(os.path.join(upload_folder, filename))
            return {'name': file.filename, 'profile_img': user.profile_img}


@ns.route('/<string:filename>')
class UploadFiles(Resource):
    def get(self, filename):
        return send_from_directory(upload_folder, filename)
