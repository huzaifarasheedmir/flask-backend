import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 20
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    PORT = 8081
    DEV_DB_PARAMS = {
        'DB_USER': "root",
        'DB_PASSWORD': "123456789",
        'DB_HOST': '127.0.0.1:3306',
        'DB_DATABASE': "mydb"
    }
    MYSQL_DB = "mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}".format(**DEV_DB_PARAMS)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or MYSQL_DB


class TestingConfig(Config):
    TESTING = True
    PORT = 1000
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    FIXTURES_DIR = os.path.join(BASE_DIR, 'tests/fixtures')


class ProductionConfig(Config):
    PORT = 8080
    PROD_DB_PARAMS = {
        'DB_USER': "root",
        'DB_PASSWORD': "123456789",
        'DB_HOST': '127.0.0.1:3306',
        'DB_DATABASE': "mydb"
    }
    MYSQL_DB = "mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}".format(**PROD_DB_PARAMS)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or MYSQL_DB


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
