from flask import request
from flask_restplus import Namespace, fields, Resource

from .user import userschema

ns = Namespace('todo', description='Todo\'s related endpoint operations.')
todoschema = ns.model(
    'Todo',
    {
        'name': fields.String(required=True, min_length=2),
        'user': fields.Nested(userschema, skip_none=True),
    },
)


@ns.route('/<int:id>')
@ns.param('id', 'Todo\'s intifier')
@ns.response(404, 'No todo found with the provided id.')
class TodoResource(Resource):
    def get(self, id):
        return 'GET a single todo'

    def patch(self, id):
        return 'PATCH a todo'

    def delete(self, id):
        return 'DELETE a todo.'


@ns.route('/')
class TodoListResource(Resource):
    def get(self):
        return 'GET all todods'

    def post(self):
        return 'POST a new todo'
