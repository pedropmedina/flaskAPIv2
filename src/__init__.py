from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from .models import db

bcrypt = Bcrypt()


def create_app():
    # app instance
    app = Flask(__name__)

    # db initialization
    db.init_app(app)

    # db migration
    Migrate(db, app)

    # bcrypt initialization
    bcrypt.init_app(app)

    return app
