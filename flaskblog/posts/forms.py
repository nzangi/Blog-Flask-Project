from wtforms import StringField, SubmitField,TextAreaField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class PostForm(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired()])
    content = TextAreaField('Post Content', validators=[DataRequired()])
    submit_post = SubmitField("Post")