
import secrets, os
from flaskblog import mail
from flask import url_for, current_app
from PIL import Image
from flask_mail import Message

def save_picture(form_picture):
    # Crée un nom de fichier random avec le module secrets
    random_hex = secrets.token_hex(8)
    # récupère le nom de fichier et l'extension
    # on ne se sert pas du nom de fichier donc 
    # on peut mettre un _ au lieu de nommer la variable
    _, f_ext = os.path.splitext(form_picture.filename)
    # construit le filename
    picture_fn = random_hex + f_ext
    # app.root_path renvoie le path de notre package directory (notre app)
    picture_path = os.path.join(current_app.root_path, "static/profile_pics", picture_fn)
    # Resize with Pillow Module (Image)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    # save data from form
    i.save(picture_path)
    return picture_fn

def send_reset_email(user):
    #On récupère le token depuis l'instance User
    token = user.get_reset_token()
    #Crée le message avec la classe Message
    # Attention : il faut avoir un mail appartenant au domaine pour aps finir dans les spam
    msg = Message('Password Reset Request', 
        sender='vmatheron.dev@gmail.com', 
        recipients=[user.email])
    msg.body = f"""To reset your password, please visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then please ignore this email and no changes will be made.
""" 
    mail.send(msg)