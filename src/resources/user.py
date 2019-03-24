from flask_restplus import Namespace, fields, Resource
from flask import request, make_response, g
from werkzeug.utils import secure_filename

from ..models import db
from ..models.user import User
from ..helpers.authorization import Authorization

ns = Namespace('user', description='/users related requests')
user_fields_default = ns.model(
    'User',
    {
        'username': fields.String(required=True, min_length=5, max_length=50),
        'email': fields.String(required=True),
        'public_id': fields.String,
        'password': fields.String,
        'profile_img': fields.String,
    },
)


@ns.route('/<public_id>', endpoint='user_resource')
@ns.param('public_id', 'User\'s public identifier')
@ns.response(404, 'No user found with given identifier')
class UserResource(Resource):
    @Authorization.authorize_user
    @ns.marshal_with(user_fields_default, envelope='data', skip_none=True)
    def get(self, public_id):
        if g.user['public_id'] != public_id and not g.user['admin']:
            ns.abort(401, custom='You don\'t have access to this info.')

        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            ns.abort(404, custom='No user found with the provided identifier.')
        return user

    @Authorization.authorize_user
    @ns.response(204, 'User was deleted.')
    def delete(self, public_id):
        if g.user['public_id'] != public_id and not g.user['admin']:
            ns.abort(401, custom='No user found with the provided identifier.')

        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            ns.abort(404, custom='You don\'t have access to this info.')
        db.session.delete(user)
        db.session.commit()
        return make_response('', 204)  # No Content

    @Authorization.authorize_user
    @ns.marshal_with(user_fields_default, envelope='data', skip_none=True)
    def patch(self, public_id):
        if g.user['public_id'] != public_id and not g.user['admin']:
            ns.abort(401, custom='No user found with the provided identifier.')

        user = User.query.filter_by(public_id=public_id).first()
        if not user:
            ns.abort(404, custom='No user found with the provided id.')

        data = request.json
        username = data.get('username')
        email = data.get('email')

        if username is not None:
            user.username = username
        if email is not None:
            user.email = email

        db.session.commit()
        return user


@ns.route('/', endpoint='user_list_resource')
class UserListResource(Resource):
    @Authorization.authorize_user
    @Authorization.authorize_admin
    @ns.marshal_list_with(user_fields_default, envelope='data', skip_none=True)
    def get(self):
        users = User.query.all()
        return users

    @ns.expect(user_fields_default, validate=True)
    @ns.response('201', 'User was successfully created.')
    def post(self):
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
        if user:
            response_dict = {
                'status': 'fail',
                'message': 'User already exists. Please login.',
            }
            return response_dict, 409  # Conflict
        else:
            new_user = User(
                username=data['username'],
                email=data['email'],
                password=data['password'],
            )
            db.session.add(new_user)
            db.session.commit()
            token = User.jwt_encode(user_id=new_user.id)
            return ({'status': 'success', 'message': token}, 201)  # Created
