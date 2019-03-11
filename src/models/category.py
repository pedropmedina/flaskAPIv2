from . import db


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    todos = db.relationship('Todo', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category({self.name})>'
