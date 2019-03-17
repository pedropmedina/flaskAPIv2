from flask import request
from flask_restplus import Namespace, Resource, fields

from ..helpers.authentication import Auth

ns = Namespace('auth', description='/auth related operations.')
login_default_fields = ns.model(
    'Login',
    {
        'username': fields.String(min_length=3, required=True),
        'password': fields.String(min_length=5, required=True),
    },
)

wrong_credentials = 'username or password do not match. Try again.'


@ns.route('/login')
@ns.response(401, wrong_credentials)
class UserLogin(Resource):
    '''
    Login users resources
    '''

    @ns.expect(login_default_fields, validate=True)
    def post(self):
        '''
        Handle login operations and return token in the body of the response
        '''
        data = request.json
        return Auth.login_user_helper(
            username=data['username'], password=data['password']
        )


@ns.route('/logout')
class UserLogout(Resource):
    '''
    Logout related methods
    '''

    def post(self):
        '''
        Handle logout operations returning user information or err msg
        '''
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user_helper(auth_header)
