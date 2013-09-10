from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from settings import database_path
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_path

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

import whereatdrexel.views
