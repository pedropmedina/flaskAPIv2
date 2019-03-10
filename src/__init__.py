from flask import Flask
from flask_migrate import Migrate

from .models import db


def create_app():
    # app instance
    app = Flask(__name__)

    # db intialization
    db.init_app(app)

    # db migration
    Migrate(db, app)

    return app
