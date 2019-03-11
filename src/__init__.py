from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from .config import envsconfig

bcrypt = Bcrypt()


def create_app(env='dev'):
    from .models import db
    from .models.user import User
    from .models.todo import Todo
    from .models.category import Category

    # app instance
    app = Flask(__name__)

    # configure app
    app.config.from_object(envsconfig[env])

    # db initialization
    db.init_app(app)

    # db migration
    Migrate(app, db)

    # bcrypt initialization
    bcrypt.init_app(app)

    return app
