import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DB_NAME = ''
    DB_USERNAME = ''
    DB_PASSWORD = ''
    DB_HOST = ''
    DB_URI = ''
    SQLALCHEMY_DATABASE_URI = ''
    PAGINATION_PAGE_SIZE = 5
    PAGINATION_PAGE_ARGUMENT_NAME = 'page'


class DevConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SWAGGER_URL = '/swagger'


class TestConfig(Config):
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_NAME = os.getenv('DB_NAME_TEST')


class ProdConfig(Config):
    SWAGGER_URL = None


secret_key = Config.SECRET_KEY
envsconfig = dict(dev=DevConfig, test=TestConfig, prod=ProdConfig)
