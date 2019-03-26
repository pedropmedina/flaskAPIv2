from flask import current_app, url_for


class PaginationHelper:
    def __init__(self, request, query, resource_url_for, user_id):
        self.request = request
        self.query = query
        self.resource_url_for = resource_url_for
        self.user_id = user_id
        self.page_size = current_app.config['PAGINATION_PAGE_SIZE']
        self.page_argument_name = current_app.config['PAGINATION_PAGE_ARGUMENT_NAME']

    def paginate_query(self):
        # get page number from request.args with get method
        # https://werkzeug.palletsprojects.com/en/0.15.x/datastructures/#werkzeug.datastructures.MultiDict.get
        page_number = self.request.args.get(self.page_argument_name, 1, type=int)
        # use flask_sqlalchemy paginate method with provided instance attributes
        # http://flask-sqlalchemy.pocoo.org/2.3/api/#flask_sqlalchemy.Pagination
        # http://flask-sqlalchemy.pocoo.org/2.3/api/#flask_sqlalchemy.BaseQuery.paginate
        paginated_results = self.query.filter_by(user_id=self.user_id).paginate(
            page_number, per_page=self.page_size, error_out=False
        )
        # setup previous and next page
        previous_page_url = (
            url_for(self.resource_url_for, page=page_number - 1, _external=True)
            if paginated_results.has_prev
            else None
        )

        next_page_url = (
            url_for(self.resource_url_for, page=page_number + 1, _external=True)
            if paginated_results.has_next
            else None
        )
        # return dict with current query result, previos, next and total count
        return {
            'results': paginated_results.items,
            'previous': previous_page_url,
            'next': next_page_url,
            'count': paginated_results.total,
        }
