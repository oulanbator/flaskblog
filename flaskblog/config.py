import os

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    #CONFIGURATION D'UN COMPTE MAIL DANS NOTRE APP !
    MAIL_SERVER = 'smtp.googlemail.com' # smtp.gmail.com ?
    MAIL_PORT = 587 # 465 ?
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')