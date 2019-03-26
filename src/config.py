import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    PAGINATION_PAGE_SIZE = 2
    PAGINATION_PAGE_ARGUMENT_NAME = 'page'
    UPLOAD_FOLDER = (
        '/Users/pedropmedina/Documents/playground/python/flask/flaskAPIv2/src/uploads'
    )
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


class DevConfig(Config):
    DB_NAME = os.getenv('DB_NAME')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_URL = '/swagger'


class TestConfig(Config):
    DB_NAME = os.getenv('DB_NAME_TEST')
    DB_USERNAME = os.getenv('DB_USERNAME_TEST')
    DB_PASSWORD = os.getenv('DB_PASSWORD_TEST')
    DB_HOST = os.getenv('DB_HOST_TEST')
    DB_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_DATABASE_URI = DB_URI
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    # Disable CSRF (Cross-site request forgery)
    # https://en.wikipedia.org/wiki/Cross-site_request_forgery
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost.localdomain'


class ProdConfig(Config):
    SWAGGER_URL = None


upload_folder = Config.UPLOAD_FOLDER
allowed_extensions = Config.ALLOWED_EXTENSIONS
secret_key = Config.SECRET_KEY

envsconfig = dict(dev=DevConfig, test=TestConfig, prod=ProdConfig)
