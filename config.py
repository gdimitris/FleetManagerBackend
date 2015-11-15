__author__ = 'dimitris'

import os

#Flask Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = 'asdolfjniasdfnglansdfgndasfngjklsdlfglmadflm'
PREFERRED_URL_SCHEME = 'https'

#SqlAlchemy Configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'fleet_manager.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

#Cache Configuration
CACHE_TYPE = 'simple'

