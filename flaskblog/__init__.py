# save this as app.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
SECRET_KEY = os.getenv('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blogpost.db"
if SECRET_KEY is not None:
    app.config['SECRET_KEY'] = SECRET_KEY
else:
    app.config['SECRET_KEY'] = '213923aec9184951d2f628c16c4d1c67'
db = SQLAlchemy(app)

from flaskblog import routes
