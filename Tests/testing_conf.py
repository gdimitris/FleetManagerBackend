import os

basedir = os.path.abspath(os.path.dirname(__file__))
TESTING = True

SERVER_NAME = '127.0.0.1'
SECRET_KEY = 'key'

DB_NAME = 'test_db.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, DB_NAME)