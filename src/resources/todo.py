from flask import request, g
from flask_restplus import Namespace, fields, Resource

from ..models import db
from ..models.todo import Todo
from ..models.category import Category

from .user import user_fields_default, User
from .category import category_fields_default

from ..helpers.authorization import Authorization
from ..helpers.pagination import PaginationHelper

ns = Namespace('todo', description='Todo\'s related endpoint operations.')
# default field "name" required for both marshal_with and expect
todo_fields_default = ns.model(
    'Todo', {'name': fields.String(required=True, min_length=2)}
)
# Use for marshal_with
todo_fields_nested_models = ns.inherit(
    'TodoNestedModels',
    todo_fields_default,
    {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'user': fields.Nested(user_fields_default, skip_none=True),
        'category': fields.Nested(category_fields_default, skip_none=True),
    },
)
# Use for expect
todo_fields_not_nested_models = ns.inherit(
    'TodoNotNestedModels',
    todo_fields_default,
    {'category': fields.String(min_length=2, required=True)},
)
# Use for marshal_with paginated results
todo_fields_paginated_nested_models = ns.model(
    'TodoPaginated',
    {
        'results': fields.Nested(
            todo_fields_nested_models, skip_none=True, as_list=True
        ),
        'previous': fields.String(),
        'next': fields.String(),
        'count': fields.Integer,
    },
)


@ns.route('/<int:id>', endpoint='todo_resource')
@ns.param('id', 'Todo\'s intifier')
@ns.response(404, 'No todo found with the provided id.')
class TodoResource(Resource):
    @Authorization.authorize_user
    @ns.marshal_with(todo_fields_nested_models, envelope='data', skip_none=True)
    def get(self, id):
        todo = Todo.query.filter_by(id=id).filter_by(user_id=g.user['user_id']).first()
        if not todo:
            ns.abort(404, custom='No todo exists with given id')
        return todo

    @Authorization.authorize_user
    @ns.marshal_with(todo_fields_nested_models, envelope='data', skip_none=True)
    def patch(self, id):
        todo = Todo.query.filter_by(id=id).filter_by(user_id=g.user['user_id']).first()
        if not todo:
            ns.abort(404, custom='No todo exists with given id.')
        data = request.json
        name = data.get('name')
        if name:
            todo.name = name
            db.session.commit()
        return todo

    @Authorization.authorize_user
    def delete(self, id):
        todo = Todo.query.filter_by(id=id).filter_by(user_id=g.user['user_id']).first()
        if not todo:
            ns.abort(404, custom='No todo exists with given id.')
        db.session.delete(todo)
        db.session.commit()
        return {'status': 'success', 'message': 'Todo was deleted.'}


@ns.route('/', endpoint='todo_list_resource')
class TodoListResource(Resource):
    @Authorization.authorize_user
    @ns.marshal_with(
        todo_fields_paginated_nested_models, envelope='data', skip_none=True
    )
    def get(self):
        pagination_helper = PaginationHelper(
            request=request,
            query=Todo.query,
            resource_url_for='api.todo_list_resource',
            user_id=g.user['user_id'],
        )
        todos = pagination_helper.paginate_query()
        return todos

    @Authorization.authorize_user
    @ns.expect(todo_fields_not_nested_models, validate=True)
    def post(self):
        try:
            data = request.json
            todo_name = data['name']
            todo_category = data['category']

            # Query user
            user = User.query.get(g.user['user_id'])
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
