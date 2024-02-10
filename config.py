import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.urandom(12)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopementConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')


class TestingConfig(BaseConfig):
    TESTING = True,
    DEBUG = True,
    SQLALCHEMY_DATABASE_URI =  'sqlite:///' + os.path.join(basedir, 'app_test.db')


class ProdactionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
