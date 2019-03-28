from datetime import datetime, timedelta
from uuid import uuid4
import re
import jwt

from . import db
from .. import bcrypt
from ..config import secret_key
from .blacklist import Blacklist
from .todo import Todo


class User(db.Model):
    '''
    User Model to create user table
    '''

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(255), unique=True, default=str(uuid4()))
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hash_password = db.Column(db.String(100), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    todos = db.relationship(Todo, backref='user', lazy=True, cascade='delete')
    profile_img = db.Column(db.String, unique=True)

    @property
    def password(self):
        raise AttributeError('password is write only')

    @password.setter
    def password(self, password):
        # hash password and return string as function returns <class 'bytes'>
        self.hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.hash_password, password)

    @classmethod
    def check_password_strength(cls, password):
        # check password is between range 8 to 32
        if len(password) < 8:
            return ('Password is too short. Must be at leaset 8 characters.', False)
        if len(password) > 32:
            return ('Password is too long. Must be less than 32 characters.', False)
        # check password includes one uppercase and lowercase character
        if re.search('[A-Z]', password) is None:
            return ('Password must include at least an uppercase character.', False)
        if re.search('[a-z]', password) is None:
            return ('Password must include at least a lowercase character.', False)
        # check password includes one symbol
        if re.search(r'[!#$%&\'()*+,-./[\\\]^_`{|}~"\]]', password) is None:
            return ('Password must include at least one symbol.', False)
        return ('', True)

    @staticmethod
    def jwt_encode(user_id):
        payload = {
            'sub': user_id,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=1),
        }
        # jwt.encode returns <class 'bytes'>, must decode to send in response as str
        return jwt.encode(payload, secret_key, algorithm='HS256').decode('utf-8')

    @staticmethod
    def jwt_decode(token):
        '''
        Decode provided token.
        If error, return type string <class 'str'>,
        else return user id <class 'int'>.
        In the auth resource, check instance and
        respond in accordance to the type.
        '''
        try:
            # Ckeck if token is blacklisted, and if so send err msg, else send sub int
            is_blacklisted = Blacklist.check_blacklist(token)
            if is_blacklisted:
                return 'Token is blacklisted. Login again.'
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Token has expired. Login again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Login again.'
