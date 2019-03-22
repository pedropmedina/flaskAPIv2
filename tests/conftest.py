import pytest

# from dotenv import load_dotenv

from src.models import db
from src import create_app
from src.models.user import User


@pytest.fixture(scope='module')
def new_user():
    user = User(username='jamesadams', email='james@gmail.com', password='pass123')
    return user


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def application():
    # Beginning of setup code
    app = create_app(env='test')
    with app.app_context():
        db.create_all()
        # End of setup code
        # Test starts running here
        yield app
        # Test finished running here
        # Beginning of teardown here
        db.session.remove()
        db.drop_all()
        # End of teardown here


@pytest.fixture
def client(application):
    return application.test_client()
