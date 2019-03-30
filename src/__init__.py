from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from src.config import envsconfig

bcrypt = Bcrypt()


def create_app(env='prod'):
    from src.models import db
    from src.models.user import User
    from src.models.todo import Todo
    from src.models.category import Category
    from src.models.blacklist import Blacklist
    from src.resources import bp

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

    # register blueprint
    app.register_blueprint(bp)

    return app
