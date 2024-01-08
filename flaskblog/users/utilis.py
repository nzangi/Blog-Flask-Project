import secrets, os
from PIL import Image
from flask_mail import Message
from flaskblog import app, mail
from flask import url_for


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(app.root_path, 'static/profile_images', picture_filename)
    output_size = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)

    return picture_filename


def send_reset_email(user):
    token = user.get_reset_token()
    message = Message("Password Reset Request", sender='noreply@demo.com', recipients=[user.email])
    message.body = f'''To reset your password, follow the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make the changes, just ignore this email and no change will be made.
'''
    mail.send(message)
    return 'Sent'
