from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = "6023ea02366af26f4d0b13335e6c52d3"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

#CONFIGURATION D'UN COMPTE MAIL DANS NOTRE APP !
# smtp.gmail.com ?
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# 465 ?
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
#WARNING : Ces deux derniers paramètres devraient être passés par une variable d'environnement
app.config['MAIL_USERNAME'] = 'vmatheron.dev@gmail.com'
app.config['MAIL_PASSWORD'] = 'Aze&124816'
# Initialisation
mail = Mail(app)

from flaskblog import routes