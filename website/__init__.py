from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail,Message

db = SQLAlchemy()
ma = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET KEY'] = "usbsusjjua"
    app.secret_key = 'super secret key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'bcs_201819@iiitm.ac.in',
    MAIL_PASSWORD = 'Dcop@126'))

    from .models import Note,User
    db.init_app(app)
    ma.init_app(app)
    create_database(app)

    from .views import view
    from .auth import auth
    from .email import mail
    app.register_blueprint(mail,prefix_url = '/')
    app.register_blueprint(view,prefix_url = '/')
    app.register_blueprint(auth,prefix_url = '/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/database.db'):
        db.create_all(app = app)
