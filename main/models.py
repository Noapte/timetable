# -*- coding: utf-8 -*-

from flask_security import UserMixin, RoleMixin

from . import db


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

shops_users = db.Table(
    'shops_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('shop_id', db.Integer(), db.ForeignKey('shop.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80, convert_unicode=True), unique=True)

    def __str__(self):
        return self.name


class Shop(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100, convert_unicode=True), unique=True)
    start_time = db.Column(db.Time())
    end_time = db.Column(db.Time())
    shift_length = db.Column(db.Time())
    timetables = db.relationship("Timetable", back_populates="shop")

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Timetable(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    json = db.Column(db.String())
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
    shop = db.relationship("Shop", back_populates="timetables")

    def __str__(self):
        return "{}-{}".format(self.year, self.month)


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(100, convert_unicode=True))
    last_name = db.Column(db.String(100, convert_unicode=True))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    shops = db.relationship('Shop', secondary=shops_users, backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.username

    def to_json(self):
        return {
            "id": self.id,
            "name": self.username
        }
