from datetime import datetime

from . import db


class Blacklist(db.Model):
    '''
    Model to keep track of blacklisted tokens
    '''

    __tablename__ = 'blacklist'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False, default=datetime.now())

    @classmethod
    def check_blacklist(cls, token):
        token = cls.query.filter_by(token=token).first()
        if token:
            return True
        return False
