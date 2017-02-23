# -*- coding: utf-8 -*-

from flask import abort, url_for, redirect, request
from flask_admin import AdminIndexView, expose
from flask_admin.contrib import sqla
from flask_security import current_user

from . import db
from models import User, Timetable, Shop


class AdminLoginIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('security.login'))
        return super(AdminLoginIndexView, self).index()


class AdminModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        return current_user.has_role('Admin')

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))


class UsersView(AdminModelView):

    excluded_list_columns = ['password']

    column_labels = {
        'username': u'Nazwa użytkownika',
        'first_name': u'Imię',
        'last_name': u'Nazwisko',
        'email': u'Email',
        'password': u'Hasło',
        'active': u'Aktywny',
        'roles': u'Role',
        'shops': u'Sklepy',
    }

    def __init__(self):
        super(UsersView, self).__init__(User, db.session, name=u"Pracownicy")


class ShopsView(AdminModelView):

    column_labels = {
        'name': u'Nazwa',
        'start_time': u'Godzina otwarcia',
        'end_time': u'Godzina zamknięcia',
        'shift_length': u'Długość zmiany',
        'timetables': u'Lista grafików',
        'users': u"Pracownicy"
    }

    def __init__(self):
        super(ShopsView, self).__init__(Shop, db.session, name=u"Salony")


class TimetablesView(AdminModelView):

    excluded_list_columns = ['json']

    column_labels = {
        'year': u'Rok',
        'month': u'Miesiąc',
        'shop': u'Salon',
    }

    def __init__(self):
        super(TimetablesView, self).__init__(Timetable, db.session, name=u"Lista grafików")
