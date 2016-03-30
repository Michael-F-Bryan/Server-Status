from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    
    # Attach routes and custom error pages
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .status import status as status_blueprint
    app.register_blueprint(status_blueprint, url_prefix='/status')

    from .files import files as files_blueprint
    app.register_blueprint(files_blueprint, url_prefix='/files')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    if app.debug is not True:   
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
                app.config.get('LOG_FILE') or 'Status.log', 
                maxBytes=1024 * 1024 * 100, 
                backupCount=20)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s: %(message)s",
                datefmt='%Y/%m/%d %I:%M:%S %p')
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)

        # Catch the requests behind the scenes from werkzeug
        logger = logging.getLogger('werkzeug')
        logger.addHandler(file_handler)

    return app
