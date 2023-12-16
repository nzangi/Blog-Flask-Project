# save this as app.py
import os
from flask import Flask, url_for, redirect, flash
from flask import render_template, url_for
from forms import SignUpForm, SignInForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Integer, String, Column

app = Flask(__name__)
SECRET_KEY = os.getenv('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blogpost.db"
if SECRET_KEY is not None:
    app.config['SECRET_KEY'] = SECRET_KEY
else:
    app.config['SECRET_KEY'] = '213923aec9184951d2f628c16c4d1c67'
db = SQLAlchemy(app)


# creating db tables
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(15), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}','{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


with app.app_context():
    db.create_all()

posts = [
    {
        'author': 'Nzangi',
        'title': 'Blog post 1',
        'content': 'First Blog Post',
        'date': 'Dec 8 2023'
    },
    {
        'author': 'Muoki',
        'title': 'Blog post 2',
        'content': 'Second Blog Post',
        'date': 'Dec 7 2023'
    },
    {
        'author': 'Kanee',
        'title': 'Blog post 3',
        'content': 'Third Blog Post',
        'date': 'Dec 6 2023'
    },
    {
        'author': 'Munyoki',
        'title': 'Blog post 4',
        'content': 'Fourth Blog Post',
        'date': 'Dec 4 2023'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title="About")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html', title="Sign Up", form=form)


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        if form.username.data == "nzangi" and form.password.data == "12345678":
            flash(f'{form.username.data} you have been logged in, welcome!', 'success')
            return redirect(url_for('home'))
        else:
            flash("Sign in unsuccessful,please recheck username and password", 'danger')
    return render_template('signin.html', title="Sign In", form=form)


if __name__ == '__main__':
    app.run(debug=True)
