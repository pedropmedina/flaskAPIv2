from functools import wraps
from flask import request, g

from .authentication import Authentication


class Authorization:
    @staticmethod
    def authorize_user(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            data, status_code = Authentication.get_current_user_helper(request)
            user_info = data.get('data')

            # return early with errors
            if not user_info:
                return data, status_code

            # save user to the g object
            g.user = user_info

            return func(*args, **kwargs)

        return decorated

    @staticmethod
    def authorize_admin(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            if not g.user['admin']:
                return (
                    {'status': 'fail', 'message': 'You don\'t have admin privileges.'},
                    401,
                )

            return func(*args, **kwargs)

        return decorated
