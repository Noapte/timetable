# -*- coding: utf-8 -*-

from datetime import time
from flask_security.utils import encrypt_password

from . import app, db, user_datastore
from models import Role, Shop


def build_db():

    db.drop_all()
    db.create_all()

    wr_bielany = Shop(name=u"Wrocław-Bielany", start_time=time(8), end_time=time(19), shift_length=time(8))
    wr_olawska = Shop(name=u"Wrocław-Oławska", start_time=time(8), end_time=time(19), shift_length=time(8))

    roles = [
        Role(name=u'Admin'),
        Role(name=u'Kierownik'),
        Role(name=u'Zastępca kierownika'),
        Role(name=u'Starszy sprzedawca'),
        Role(name=u'Sprzedawca'),
    ]

    employees = [
        (u"Fredynand", u"Kiepski", roles[1], wr_bielany),
        (u"Marian", u"Paździoch", roles[2], wr_bielany),
        (u"Arnold", u"Boczek", roles[3], wr_bielany),
        (u"Waldemar", u"Kiepski", roles[4], wr_bielany),
        (u"Janusz", u"Socha", roles[4], wr_bielany),

        (u"Władysław", u"Słoik", roles[1], wr_olawska),
        (u"Alojzy", u"Pęduszko", roles[2], wr_olawska),
        (u"Barbara", u"Kwarc", roles[3], wr_olawska),
        (u"Izaak", u"Rosenfeld", roles[4], wr_olawska),
        (u"Grażyna", u"Janusz", roles[4], wr_olawska),
    ]

    with app.app_context():

        db.session.add(wr_bielany)
        db.session.add(wr_olawska)
        db.session.commit()

        for role in roles:
            db.session.add(role)
        db.session.commit()

        for first_name, last_name, role, shop in employees:
            username = first_name[0].lower() + last_name.lower()
            user_datastore.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=username + u"@militaria.pl",
                password=encrypt_password(username),
                roles=[role],
                shops=[shop]
            )
        db.session.commit()

        user_datastore.create_user(
            username='admin',
            first_name='Admin',
            email='webapplicationmailservice@gmail.com',
            password=encrypt_password('admin'),
            roles=[roles[0]]
        )
        db.session.commit()
