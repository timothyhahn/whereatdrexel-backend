## Flask Dependencies
from flask import Flask

## App Dependencies
from .extensions import db, bcrypt, login_manager
from .admin import admin
from .api import api

EXTENSIONS = (db, bcrypt, login_manager)
BLUEPRINTS = (admin, api)


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    for b in BLUEPRINTS:
        app.register_blueprint(b)

    for e in EXTENSIONS:
        e.init_app(app)

    return app
