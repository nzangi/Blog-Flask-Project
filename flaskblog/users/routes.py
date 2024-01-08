from flask import Blueprint

from flaskblog.users.forms import SignUpForm, SignInForm, UpdateAccountForm, RequestResetForm, PasswordResetForm
from flask import redirect, flash, render_template, url_for, request
from flaskblog.models import User, Post
from flaskblog import bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.users.utilis import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successful, you can now login!', 'success')
        return redirect(url_for('users.signin'))
    return render_template('signup.html', title="Sign Up", form=form)


@users.route("/signin", methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash(f'{form.username.data} you have been logged in, welcome!', 'success')
            next_page = request.args.get('next')
            print(next_page)
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please recheck email and password', 'danger')
    return render_template('signin.html', title='Login', form=form)


@users.route("/signout")
def signout():
    flash('You have successfully logged out', 'danger')
    logout_user()
    return redirect(url_for('users.signin'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account details were updated successfully!")
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_images/' + current_user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("user_posts.html", posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been send with instructions to reset your password", 'success')
        return redirect(url_for('users.signin'))
    return render_template("reset_request.html", title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an Invalid or expired token", 'warning')
        return redirect(url_for('users.reset_request'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been changed  successfully, you can now login!', 'success')
        return redirect(url_for('users.signin'))
    return render_template("reset_token.html", title='Reset Password', form=form)
