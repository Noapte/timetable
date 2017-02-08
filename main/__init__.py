# -*- coding: utf-8 -*-
import os

from flask import Flask, url_for
from flask_admin import Admin, helpers
from flask_mail import Mail
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
mail = Mail(app)


import models
import views
import forms


user_datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore, login_form=forms.ExtendedLoginForm)


admin = Admin(
    app,
    'Militaria.pl',
    index_view=views.AdminLoginIndexView(),
    base_template='base.html',
    template_mode='bootstrap3'
)

admin.add_view(views.AdminTimetableView(name="Grafik", endpoint='table'))
admin.add_view(views.AdminModelView(models.Shop, db.session))
admin.add_view(views.AdminModelView(models.Timetable, db.session))
admin.add_view(views.UsersView(models.User, db.session))


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
# utils.build_db()
