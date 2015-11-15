__author__ = 'dimitris'

from Application import db


class Users(db.Model):
    __tablename__ = 'Users'

    phone_id = db.Column(db.String(80), nullable=False, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)


class LocationPoints(db.Model):
    __tablename__ = 'LocationPoints'

    phone_id = db.Column(db.String(80), db.ForeignKey('Users.phone_id'), primary_key=True)
    latitude = db.Column(db.Float(precision=7))
    longitude = db.Column(db.Float(precision=7))