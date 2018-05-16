from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
mongo = MongoEngine()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def format_time(value):
    return value.strftime("%Y-%m-%d %H:%M:%S")

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)



    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    mongo.init_app(app)
    login_manager.init_app(app)

    app.jinja_env.filters['format_time'] = format_time

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .feed import feed as feed_blueprint
    app.register_blueprint(feed_blueprint, url_prefix='/f')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    return app
