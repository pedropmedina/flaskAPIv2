from flask_restplus import Api
from flask import Blueprint

from .user import ns as ns_user

bp = Blueprint('api', __name__, url_prefix='/api/v1')

api = Api(
    bp,
    version='1.0',
    title='Todo API with user authentication',
    description='A todo API with basic operations',
)


api.add_namespace(ns_user, path='/users')
