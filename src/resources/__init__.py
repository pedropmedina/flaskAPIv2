from flask_restplus import Api
from flask import Blueprint

from .user import ns as ns_user
from .todo import ns as ns_todo
from .category import ns as ns_category
from .auth import ns as ns_auth
from .upload import ns as ns_upload

bp = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(
    bp,
    version='1.0',
    title='Todo API with user authentication',
    description='A todo API with basic operations',
)


api.add_namespace(ns_user, path='/users')
api.add_namespace(ns_todo, path='/todos')
api.add_namespace(ns_category, path='/categories')
api.add_namespace(ns_auth, path='/auth')
api.add_namespace(ns_upload, path='/uploads')
