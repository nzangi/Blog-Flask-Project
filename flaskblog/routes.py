from flask import redirect, flash, render_template, url_for, request
from flaskblog.forms import SignUpForm, SignInForm, UpdateAccountForm
from flaskblog.models import User, Post
from flaskblog import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required
import secrets, os
from PIL import Image

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
            next_page = request.args.get('next')
            print(next_page)
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please recheck email and password', 'danger')
    return render_template('signin.html', title='Login', form=form)


@app.route("/signout")
def signout():
    flash('You have successfully logged out', 'danger')
    logout_user()
    return redirect(url_for('signin'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_extsnsion = os.path.splitext(form_picture.filename)
    picture_filename= random_hex + file_extsnsion
    picture_path = os.path.join(app.root_path,'static/profile_images',picture_filename)
    output_size = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)




    return picture_filename

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file= save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account details were updated successfully!")
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_images/' + current_user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form)
