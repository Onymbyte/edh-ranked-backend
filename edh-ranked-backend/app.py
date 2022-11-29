from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager
from sqlalchemy import create_engine

from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap5

app = Flask(__name__)
app.debug = True

with open('config.txt', 'r') as f:
    lines = f.readlines()
    app.config['SECRET_KEY'] = lines[0]
    app.config['SQLALCHEMY_DATABASE_URI'] = lines[1]

app.config['sqlalchemy_track_modifications'.upper()] = False
app.jinja_env.filters['zip'] = zip


db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

bootstrap = Bootstrap5(app)

from models import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
from routes import *