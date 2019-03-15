from flask import request
from flask_restplus import Namespace, fields, Resource

from ..models import db
from ..models.todo import Todo
from .user import user_fields_default, User

ns = Namespace('todo', description='Todo\'s related endpoint operations.')
todo_fields_default = ns.model(
    'Todo', {'name': fields.String(required=True, min_length=2)}
)
todo_fields_nested_user = todo_fields_default.clone(
    'TodoNestedUser', {'user': fields.Nested(user_fields_default, skip_none=True)}
)
todo_fields_user_publicid = todo_fields_default.clone(
    'TodoUserPublicId', {'user': fields.String(required=True)}
)


@ns.route('/<int:id>')
@ns.param('id', 'Todo\'s intifier')
@ns.response(404, 'No todo found with the provided id.')
class TodoResource(Resource):
    @ns.marshal_with(todo_fields_nested_user, envelope='data', skip_none=True)
    def get(self, id):
        todo = Todo.query.get(id)
        if not todo:
            ns.abort(404, custom='No todo exists with given id')
        return todo

    @ns.marshal_with(todo_fields_nested_user, skip_none=True)
    def patch(self, id):
        todo = Todo.query.get(id)
        if not todo:
            ns.abort(404, custom='No todo exists with given id.')
        data = request.json
        name = data.get('name')
        if name:
            todo.name = name
        return todo

    def delete(self, id):
        return 'DELETE a todo.'


@ns.route('/')
class TodoListResource(Resource):
    @ns.marshal_list_with(todo_fields_nested_user, envelope='data', skip_none=True)
    def get(self):
        todos = Todo.query.all()
        return todos

    @ns.expect(todo_fields_user_publicid, validate=True)
    def post(self):
        try:
            data = request.json
            todo_name = data['name']
            user_public_id = data['user']

            # Query user
            user = User.query.filter_by(public_id=user_public_id).first()
            if not user:
                ns.abort(404, custom='No user found with provided id.')

            todo = Todo(name=todo_name, user=user)
            db.session.add(todo)
            db.session.commit()
            res_dict = {'status': 'success', 'message': 'Todo was created.'}
            return res_dict, 201  # Created
        except Exception as err:
            db.session.rollback()
            return {'status': 'fail', 'message': str(err)}, 400
