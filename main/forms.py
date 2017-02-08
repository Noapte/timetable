# -*- coding: utf-8 -*-

from flask_security.forms import LoginForm
from wtforms import StringField, PasswordField


class ExtendedLoginForm(LoginForm):

    email = StringField('Login lub email:')
    password = PasswordField(u'Hasło')
