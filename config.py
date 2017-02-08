# -*- coding: utf-8 -*-

SECRET_KEY = '123456790'

DATABASE_FILE = 'sample_db.sqlite'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE
SQLALCHEMY_ECHO = True

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'webapplicationmailservice@gmail.com'
MAIL_PASSWORD = 'javaee2014'

# Flask-Security config
SECURITY_USER_IDENTITY_ATTRIBUTES = ('email', 'username')
SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"
SECURITY_RESET_URL = "/reset/"
SECURITY_CHANGE_URL = "/change/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_RESET_VIEW = "/admin/"

# Flask-Security features
SECURITY_CHANGEABLE = True
SECURITY_RECOVERABLE = True
SECURITY_REGISTERABLE = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
