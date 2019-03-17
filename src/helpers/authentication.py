from ..models import db
from ..models.user import User
from ..models.blacklist import Blacklist


class Auth:
    # handle logging in
    @staticmethod
    def login_user_helper(username, password):
        '''
        Authentication helper to be used at login.
        '''
        user = User.query.filter_by(username=username).first()
        is_password_correct = user.check_password(password=password)

        if not user or not is_password_correct:
            return {'status': 'fail', 'message': 'Wrong credentials. Try again.'}

        token = User.jwt_encode(user_id=user.id)

        return {
            'status': 'success',
            'message': 'Successfully logged in.',
            'Authorization': f'Bearer {token}',
        }

    # handle logging out
    @staticmethod
    def logout_user_helper(auth_header):
        # if correct, auth_header comes in the form of 'Bearer tokenstringhere'
        if not auth_header:
            token = ''
        else:
            token = auth_header.split(' ')[1]  # isolate token string from Bearer

        if token:
            userid_or_err_msg = User.jwt_decode(token)

            # is decode returns a <class 'str'>, then it is an err
            if isinstance(userid_or_err_msg, str):
                return {'status': 'fail', 'message': userid_or_err_msg}, 401

            # save token to blacklist and return user info back to client
            blacklisted = Blacklist(token=token)
            db.session.add(blacklisted)
            db.session.commit()
            user = User.query.get(userid_or_err_msg)
            return (
                {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'username': user.username,
                        'admin': user.admin,
                        'registered_on': str(user.registered_on),
                    },
                },
            )

    # get the logged in user
    @staticmethod
    def get_current_user_helper(request):
        # get token from current_request headers
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            token = ''
        else:
            token = auth_header.split(' ')[1]

        if not token:
            return {'status': 'fail', 'message': 'No token provided'}, 400

        userid_or_err_msg = User.jwt_decode(token=token)

        if isinstance(userid_or_err_msg, str):
            return {'status': 'fail', 'message': userid_or_err_msg}, 401

        user = User.query.get(userid_or_err_msg)
        return {
            'status': 'success',
            'data': {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'admin': user.admin,
                'registered_on': str(user.registered_on),
            },
        }
