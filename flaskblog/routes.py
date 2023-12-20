from flask import redirect, flash, render_template, url_for,request
from flaskblog.forms import SignUpForm, SignInForm
from flaskblog.models import User, Post
from flaskblog import app, bcrypt, db
from flask_login import login_user, current_user, logout_user,login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successful, you can now login!', 'success')
        return redirect(url_for('signin'))
    return render_template('signup.html', title="Sign Up", form=form)


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f'{form.username.data} you have been logged in, welcome!', 'success')
            # next_page = request.args.get('next')
            # print(next_page)
            return redirect(request.args.get('next', url_for('home')))
            # return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Sign in unsuccessful,please recheck username and password", 'danger')
    return render_template('signin.html', title="Sign In", form=form)

@app.route("/signout")
def signout():
    logout_user()
    return redirect(url_for('signin'))
@app.route("/account")
@login_required
def account():
    return render_template('account.html',title="Account")
