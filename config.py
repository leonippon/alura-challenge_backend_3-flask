import os

class Config(object):
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'data/temp/')
    MAX_CONTENT_LENGTH = 0.5 * 1024 * 1024
    HASH_SALT_ROUNDS = 12
    TEST_USERS = True
    LIMIT_ACC=100000
    LIMIT_AG=100000


class ProductionConfig(Config):
    TESTING = False
    db_path = os.path.join(os.path.dirname(__file__), 'db/database.db')
    db_uri = f'sqlite:///{db_path}'
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_ECHO = False


class DevelopmentConfig(Config):
    TESTING = False
    db_path = os.path.join(os.path.dirname(__file__), 'db/database_dev.db')
    db_uri = f'sqlite:///{db_path}'
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_ECHO = False
    MAIL_SUPPRESS_SEND = True


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO = False
    MAIL_SUPPRESS_SEND = True