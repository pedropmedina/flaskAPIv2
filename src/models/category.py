from . import db


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    todos = db.relationship('Todo', backref='category', lazy=True, cascade='delete')

    def __repr__(self):
        return f'<Category({self.name})>'

    @classmethod
    def is_category_unique(cls, name, id=0):
        existing_category = cls.query.filter_by(name=name).first()
        if not existing_category:
            return (True, None)
        else:
            # SQLAlchemy will assign 0 to instances that have yet to be register to db.
            # In this case SQLAlchemy will find an instance of Category, by confirm that
            # it is a new instance by checking its id value.
            if existing_category.id == 0:
                return (True, None)
            return (False, existing_category)
