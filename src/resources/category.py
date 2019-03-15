from flask import request
from flask_restplus import Resource, Namespace, fields

ns = Namespace('category', description='Category related resources.')
category_fields_default = ns.model(
    'Category', {'name': fields.String(min_length=2, required=True)}
)


@ns.route('/<int:id>')
@ns.param('id', 'Category\'s identifier.')
@ns.response(404, 'No category found with provided id.')
class CategoryResource(Resource):
    def get(self, id):
        return 'From GET'

    def patch(self, id):
        return 'FROM PATCH'

    def delete(self, id):
        return 'From DELETE'


@ns.route('/')
class CategoryListResource(Resource):
    def get(self):
        return 'From GET'

    def post(self):
        return 'From POST'
