from flask import request
from flask_restplus import Namespace, fields, Resource

from ..models import db
from ..models.todo import Todo
from ..models.category import Category
from .user import user_fields_default, User
from .category import category_fields_default

ns = Namespace('todo', description='Todo\'s related endpoint operations.')
todo_fields_default = ns.model(
    'Todo', {'name': fields.String(required=True, min_length=2)}
)
todo_fields_nested_models = todo_fields_default.clone(
    'TodoNestedUser',
    {
        'id': fields.Integer,
        'user': fields.Nested(user_fields_default, skip_none=True),
        'category': fields.Nested(category_fields_default, skip_none=True),
    },
)
todo_fields_not_nested_models = todo_fields_default.clone(
    'TodoUserPublicId',
    {
        'user': fields.String(required=True),
        'category': fields.String(min_length=2, required=True),
    },
)


@ns.route('/<int:id>')
@ns.param('id', 'Todo\'s intifier')
@ns.response(404, 'No todo found with the provided id.')
class TodoResource(Resource):
    @ns.marshal_with(todo_fields_nested_models, envelope='data', skip_none=True)
    def get(self, id):
        todo = Todo.query.get(id)
        if not todo:
            ns.abort(404, custom='No todo exists with given id')
        return todo

    @ns.marshal_with(todo_fields_nested_models, envelope='data', skip_none=True)
    def patch(self, id):
        todo = Todo.query.get(id)
        if not todo:
            ns.abort(404, custom='No todo exists with given id.')
        data = request.json
        name = data.get('name')
        if name:
            todo.name = name
            db.session.commit()
        return todo

    def delete(self, id):
        todo = Todo.query.get(id)
        if not todo:
            ns.abort(404, custom='No todo exists with given id.')
        db.session.delete(todo)
        db.session.commit()
        return {'status': 'success', 'message': 'Todo was deleted.'}


@ns.route('/')
class TodoListResource(Resource):
    @ns.marshal_list_with(todo_fields_nested_models, envelope='data', skip_none=True)
    def get(self):
        todos = Todo.query.all()
        return todos

    @ns.expect(todo_fields_not_nested_models, validate=True)
    def post(self):
        try:
            data = request.json
            todo_name = data['name']
            user_public_id = data['user']
            todo_category = data['category']

            # Query user
            user = User.query.filter_by(public_id=user_public_id).first()
            if not user:
                ns.abort(404, custom='No user found with provided id.')

            # Check for existing category or create new one
            is_category_unique, existing_category = Category.is_category_unique(
                name=todo_category
            )
            if is_category_unique:
                category = Category(name=todo_category)
                db.session.add(category)
            else:
                category = existing_category

            todo = Todo(name=todo_name, user=user, category=category)
            db.session.add(todo)
            db.session.commit()
            res_dict = {'status': 'success', 'message': 'Todo was created.'}
            return res_dict, 201  # Created
        except Exception as err:
            db.session.rollback()
            return {'status': 'fail', 'message': str(err)}, 400
