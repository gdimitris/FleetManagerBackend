__author__ = 'dimitris'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cache import Cache
from flask_sslify import SSLify


app = Flask(__name__)
app.config.from_object('config')
sslify = SSLify(app, subdomains=True)
db = SQLAlchemy(app)
cache = Cache(app)


from Application import views, models