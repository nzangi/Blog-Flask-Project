from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flaskblog.models import User
from flask_login import current_user


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=15)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    signup_button = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is already taken,try another one!")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is already taken,try another one!")


class SignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember_me = BooleanField('Remember Me')
    signin_button = SubmitField('Sign In')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6, max=15)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['png', 'jpg'])])
    signup_button = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("That username is already taken,try another one!")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("That email is already taken,try another one!")


class RequestResetForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password_reset_button = SubmitField('Request Password Reset')

    def validate_email(self, email):
            user = User.query.filter_by(email=email.data).first()
            if user is None:
                raise ValidationError("There is no account with that E-mail.You must register that E-mail!")


class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    reset_password = SubmitField('Reset Password')