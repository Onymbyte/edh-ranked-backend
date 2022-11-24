from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager
from sqlalchemy import create_engine

from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL

# engine = create_engine("mysql://onymbit:rutgers28@18.188.99.73:3306/testDB")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdkhjfgkajsdhgjhdfbajvbhb'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://onymbit:rutgers28@18.188.99.73:3306/edhRanked"
app.config['sqlalchemy_track_modifications'.upper()] = False
# app.config['MYSQL_HOST'] = '18.188.99.73'
# app.config['MYSQL_PORT'] = 3306
# app.config['MYSQL_USER'] = 'onymbit'
# app.config['MYSQL_PASSWORD'] = 'rutgers28'
# app.config['MYSQL_DB'] = 'testDB'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from models import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
from routes import *
