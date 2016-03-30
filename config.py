import os

project_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my super secret key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    JAKE_MAIL_SUBJECT_PREFIX = '[Jake]'
    JAKE_MAIL_SENDER = 'CottonBud <cottonbud315@gmail.com>'
    JAKE_ADMIN = os.environ.get('JAKE_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOW_REGISTRATION = os.environ.get('ALLOW_REGISTRATION') or True

    FILE_UPLOAD_FOLDER = (os.environ.get('FILE_UPLOAD_FOLDER') or 
                          os.path.join(project_dir, 'file_uploads'))

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
            'sqlite:///' + os.path.join(project_dir, 'data-dev.sqlite')
    # POSTGRES_USER = 'postgres'
    # POSTGRES_PASS = os.environ.get('POSTGRES_PASS') or 'password'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    #         'postgresql+psycopg2://{}:{}@localhost:5432/jake_dev'.format(
    #         POSTGRES_USER, POSTGRES_PASS)


class TestingConfig(Config):
    LOG_FILE = 'Jake_testing.log'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
            'sqlite:///' + os.path.join(project_dir, 'data-test.sqlite')


class ProductionConfig(Config):
    LOG_FILE = 'Jake_production.log'
    ALLOW_REGISTRATION = os.environ.get('ALLOW_REGISTRATION') or False

    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL') or \
            'sqlite:///' + os.path.join(project_dir, 'data.sqlite')

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

