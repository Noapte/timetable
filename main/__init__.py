# -*- coding: utf-8 -*-
import os

from flask import Flask, url_for, redirect
from flask_admin import Admin, helpers
from flask_babelex import Babel
from flask_mail import Mail
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
mail = Mail(app)
babel = Babel(app)


import models
import views
import forms
from timetable_view import TimetableView


user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore, login_form=forms.ExtendedLoginForm)


admin = Admin(
    app,
    'Shop.pl',
    index_view=views.AdminLoginIndexView(),
    base_template='base.html',
    template_mode='bootstrap3'
)

admin.add_view(TimetableView())
admin.add_view(views.ShopsView())
admin.add_view(views.TimetablesView())
admin.add_view(views.UsersView())


@app.route('/')
def index():
    return redirect(url_for('admin.index'))


@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=helpers,
        get_url=url_for
    )


import utils

app_dir = os.path.realpath(os.path.dirname(__file__))
database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
if not os.path.exists(database_path):
    utils.build_db()
