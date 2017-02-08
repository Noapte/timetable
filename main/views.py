# -*- coding: utf-8 -*-

import json

from flask import abort, url_for, redirect, request
from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.contrib import sqla
from flask_security import current_user

from . import app, db
from models import User, Timetable


class AdminLoginIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('security.login'))
        return super(AdminLoginIndexView, self).index()


class AdminTimetableView(BaseView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_active

    def is_editable(self):
        if not self.is_accessible():
            return False

        return current_user.has_role('Admin') or current_user.has_role('Kierownik')

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('security.login'))
        return self.render('table.html')

    @expose('/get', methods=('GET', 'POST'))
    def get_table(self):
        shops = current_user.shops
        current_shop = shops[0]
        employees = [u.to_json() for u in User.query.filter(User.shops.any(id=current_shop.id)).all()]
        return json.dumps({
            "employees": employees,
            "currentShop": current_shop.to_json(),
            "availableShops": [shop.to_json() for shop in shops]})

    @expose('/add', methods=('GET', 'POST'))
    def add_table(self):
        shop = request.form.get("shop", 1)
        year = request.form.get("year", 2017)
        month = request.form.get("month", 1)
        payload = request.form.get("json", "{}")

        try:
            db.session.add(Timetable(year=year, month=month, json=payload, shop_id=shop))
            db.session.commit()
            return json.dumps({"status": "OK"})
        except Exception, e:
            return json.dumps({"error": str(e)}), 500


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


@app.route('/')
def index():
    return redirect(url_for('admin.index'))
