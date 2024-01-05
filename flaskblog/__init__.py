# save this as run.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
SECRET_KEY = os.getenv('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blogpost.db"
if SECRET_KEY is not None:
    app.config['SECRET_KEY'] = SECRET_KEY
else:
    app.config['SECRET_KEY'] = '213923aec9184951d2f628c16c4d1c67'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'signin'
login_manager.login_message_category = 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['E_MAIL'] = os.getenv('E_MAIL')
app.config['PASSWORD'] = os.getenv('PASSWORD')
mail = Mail(app)
from flaskblog import routes
