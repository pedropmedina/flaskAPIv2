import os
from dotenv import load_dotenv

load_dotenv()


def compose_database_uri(db_username, db_password, db_host, db_name):
    return f'postgresql://{db_username}:{db_password}@{db_host}/{db_name}'


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    PAGINATION_PAGE_SIZE = 2
    PAGINATION_PAGE_ARGUMENT_NAME = 'page'
    UPLOAD_FOLDER = 'src/uploads'
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    # default DB_URI to production, else use _DEV ending during development
    DB_URI = compose_database_uri(
        os.getenv('DB_USERNAME_DEV', os.environ['DB_USERNAME']),
        os.getenv('DB_PASSWORD_DEV', os.environ['DB_PASSWORD']),
        os.getenv('DB_HOST_DEV', os.environ['DB_HOST']),
        os.getenv('DB_NAME_DEV', os.environ['DB_NAME']),
    )
    SQLALCHEMY_DATABASE_URI = DB_URI


class DevConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_URL = '/swagger'


class ProdConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_URL = False


class TestConfig(Config):
    TESTING = True
    DB_URI = compose_database_uri(
        os.getenv('DB_USERNAME_TEST'),
        os.getenv('DB_PASSWORD_TEST'),
        os.getenv('DB_HOST_TEST'),
        os.getenv('DB_NAME_TEST'),
    )
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    # Disable CSRF (Cross-site request forgery)
    # https://en.wikipedia.org/wiki/Cross-site_request_forgery
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost.localdomain'


upload_folder = Config.UPLOAD_FOLDER
allowed_extensions = Config.ALLOWED_EXTENSIONS
secret_key = Config.SECRET_KEY

envsconfig = dict(dev=DevConfig, test=TestConfig, prod=ProdConfig)
