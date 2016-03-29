import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my super secret key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    JAKE_MAIL_SUBJECT_PREFIX = '[Jake]'
    JAKE_MAIL_SENDER = 'CottonBud <cottonbud315@gmail.com>'
    JAKE_ADMIN = os.environ.get('JAKE_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    LOG_FILE = 'Jake_dev.log'
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    # POSTGRES_USER = 'postgres'
    # POSTGRES_PASS = os.environ.get('POSTGRES_PASS') or 'password'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #         'postgresql+psycopg2://{}:{}@localhost:5432/jake_dev'.format(
    #         POSTGRES_USER, POSTGRES_PASS)


class TestingConfig(Config):
    LOG_FILE = 'Jake_testing.log'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    LOG_FILE = 'Jake_production.log'

    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    # POSTGRES_USER = 'postgres'
    # POSTGRES_PASS = os.environ.get('POSTGRES_PASS') or 'password'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL') or \
    #         'postgresql+psycopg2://{}:{}@localhost:5432/jake'.format(
    #         POSTGRES_USER, POSTGRES_PASS)

    @classmethod
    def init_app(cls, app):
        # Handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)


config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,

        'default': DevelopmentConfig,
}

