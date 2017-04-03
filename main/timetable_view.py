# -*- coding: utf-8 -*-

import json

from flask import abort, url_for, redirect, request
from flask_admin import BaseView, expose
from flask_security import current_user

from . import db
from models import User, Timetable, Shop


class TimetableView(BaseView):

    def __init__(self):
        super(TimetableView, self).__init__(name="Grafik", endpoint='table')

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

    def ajax_exception_handler(method):
        def _wrap(self, *args, **kwargs):
            try:
                return method(self, *args, **kwargs)
            except Exception, e:
                return json.dumps(str(e)), 500
        return _wrap

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('security.login'))
        return self.render('table.html')

    @expose('/test')
    def test(self):
        return self.render('test.html')

    @expose('/get', methods=('GET', 'POST'))
    @ajax_exception_handler
    def get_table(self):
        current_shop, available_shops = self._get_shops()

        employees = [u.to_json() for u in User.query.filter(User.shops.any(id=current_shop.id)).all()]
        schedule = {}
        for timetable in Timetable.query.filter(Timetable.shop_id == current_shop.id).all():
            if timetable.year in schedule:
                schedule[timetable.year][timetable.month] = timetable.json
            else:
                schedule[timetable.year] = {timetable.month: timetable.json}

        return self._serialize(
            edit=self.is_editable(),
            schedule=schedule,
            employees=employees,
            currentShop=current_shop.to_json(),
            availableShops=[shop.to_json() for shop in available_shops])

    @expose('/update', methods=('GET', 'POST'))
    @ajax_exception_handler
    def update_timetable(self):
        year = request.form.get("year")
        month = request.form.get("month")
        payload = request.form.get("json")

        shop, _ = self._get_shops()

        timetable = self._get_timetable(shop.id, year, month)
        if timetable:
            timetable.json = payload
        else:
            db.session.add(Timetable(year=year, month=month, json=payload, shop_id=shop.id))
        db.session.commit()
        return self._serialize(status="OK")

    def _get_shops(self):
        available_shops = current_user.shops
        if not available_shops:
            raise Exception("No shops available")

        shop_id = request.form.get("shop")
        if not shop_id:
            return available_shops[0], available_shops

        shop = Shop.query.get(shop_id)
        if shop not in available_shops:
            raise Exception("Shop unavailable")
        return shop, available_shops

    def _get_timetable(self, shop_id, year, month):
        return Timetable.query.filter(Timetable.shop_id == shop_id, Timetable.year == year, Timetable.month == month).first()

    def _serialize(self, **kwargs):
        return json.dumps(kwargs, ensure_ascii=False)
