from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager
from sqlalchemy import create_engine

from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap5
from flask_mail import Mail, Message

app = Flask(__name__)
app.debug = True

with open('config.txt', 'r') as f:
    lines = f.readlines()
    app.config['SECRET_KEY'] = lines[0]
    app.config['SQLALCHEMY_DATABASE_URI'] = lines[1].strip()
    app.config['MAIL_USERNAME'] = lines[2].strip()
    app.config['MAIL_PASSWORD'] = lines[3].strip()
    # print(lines[2].strip())
    # print(lines[3].strip())

app.config['sqlalchemy_track_modifications'.upper()] = False
app.jinja_env.filters['zip'] = zip
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

bootstrap = Bootstrap5(app)

from models import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# @app.route("/testing/")
# def testing_email():
#     msg = Message('Hello from the other side!', sender =   'edhranked@gmail.com', recipients = ['edhranked@gmail.com'])
#     msg.body = "Hey EDHRanked sending you this email from my Flask app, lmk if it works"
#     mail.send(msg)
#     return "Message sent!"
from routes import *