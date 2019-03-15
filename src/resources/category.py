from flask import request
from flask_restplus import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError

from ..models import db
from ..models.category import Category

ns = Namespace('category', description='Category related resources.')
category_fields_default = ns.model(
    'Category',
    {'id': fields.Integer, 'name': fields.String(min_length=2, required=True)},
)

category_not_found_message = 'No category found with provided id.'
duplicate_category_message = 'Category of name "{}" already exists.'


@ns.route('/<int:id>')
@ns.param('id', 'Category\'s identifier.')
@ns.response(404, category_not_found_message)
class CategoryResource(Resource):
    @ns.marshal_with(category_fields_default, envelope='data', skip_none=True)
    def get(self, id):
        category = Category.query.get(id)
        if not category:
            ns.abort(404, category_not_found_message)
        return category

    @ns.marshal_with(category_fields_default, envelope='data', skip_none=True)
    def patch(self, id):
        try:
            category = Category.query.get(id)
            if not category:
                ns.abort(404, category_not_found_message)

            data = request.json

            if 'name' in data and data['name'] is not None:
                category.name = data['name']

            db.session.commit()
            return category
        except SQLAlchemyError as err:
            db.session.rollback()
            return {'status': 'fail', 'message': str(err)}, 400

    def delete(self, id):
        try:
            category = Category.query.get(id)
            if not category:
                ns.abort(404, category_not_found_message)

            db.session.delete(category)
            db.session.commit()
            return {'status': 'success', 'message': 'category was deleted.'}
        except SQLAlchemyError as err:
            db.session.rollback()
            return {'status': 'fail', 'message': str(err)}, 400


@ns.route('/')
class CategoryListResource(Resource):
    @ns.marshal_list_with(category_fields_default, envelope='data', skip_none=True)
    def get(self):
        categories = Category.query.all()
        return categories

    @ns.expect(category_fields_default, validate=True)
    def post(self):
        try:
            data = request.json

            # Check for category uniqueness
            is_category_unique, existing_category = Category.is_category_unique(
                name=data['name']
            )

            if not is_category_unique:
                return {
                    'status': 'fail',
                    'message': duplicate_category_message.format(data['name']),
                }

            category = Category(name=data['name'])
            db.session.add(category)
            db.session.commit()
            return {'status': 'success', 'message': 'category was created.'}, 201
        except SQLAlchemyError as err:
            print(str(err))
            db.session.rollback()
            return {'status': 'fail', 'message': str(err)}, 400
