from flask import request
from flask_restplus import Resource, Namespace, fields

ns = Namespace('category', description='Category related resources.')
category_fields_default = ns.model(
    'Category', {'name': fields.String(min_length=2, required=True)}
)
