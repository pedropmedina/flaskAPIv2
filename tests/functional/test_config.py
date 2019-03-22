from src.config import envsconfig

dev = envsconfig['dev']
test = envsconfig['test']


def test_development(app):
    assert not app.config['TESTING']
    assert app.config['DB_NAME'] == dev.DB_NAME
    assert app.config['SQLALCHEMY_DATABASE_URI'] == dev.SQLALCHEMY_DATABASE_URI


def test_testing(app):
    app.config.from_object(test)
    assert app.config['TESTING'] == test.TESTING
    assert app.config['DB_NAME'] == test.DB_NAME
    assert app.config['SQLALCHEMY_DATABASE_URI'] == test.SQLALCHEMY_DATABASE_URI
