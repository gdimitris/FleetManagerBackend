__author__ = 'dimitris'

from Application import db


# class Users(db.Model):
#     __tablename__ = 'Users'
#
#     phone_id = db.Column(db.String(80), nullable=False, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     surname = db.Column(db.String(80), nullable=False)


class LocationPoints(db.Model):
    __tablename__ = 'LocationPoints'

    entry_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone_id = db.Column(db.String(80))
    timestamp = db.Column(db.DateTime, nullable=False)
    latitude = db.Column(db.Float(precision=7))
    longitude = db.Column(db.Float(precision=7))
