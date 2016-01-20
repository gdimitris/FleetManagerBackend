__author__ = 'dimitris'

import os
import urllib

#Flask Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
SECRET_KEY = 'asdolfjniasdfnglansdfgndasfngjklsdlfglmadflm'
PREFERRED_URL_SCHEME = 'https'

#SqlAlchemy Configuration

#params = urllib.quote_plus("DRIVER={SQL Server Native Client 10.0};SERVER=SCYLLA\SQLEXPRESS;DATABASE=testfm;UID=EnviousCreep;PWD=1234")
env_server_name = os.environ.get('SERVERNAME')
env_database = os.environ.get('DATABASENAME')
env_username = os.environ.get('FLEETUSERNAME')
env_password = os.environ.get('FLEETPASSWORD')

db_server = env_server_name if env_server_name else "SCYLLA\SQLEXPRESS"
database = env_database if env_database else "testfm"
username = env_username if env_username else "fleet"
password = env_password if env_password else "mitsos123!"
driver_string = "DRIVER={SQL Server Native Client 10.0};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s" % (db_server, database, username, password)
params = urllib.quote_plus(driver_string)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'fleet_manager.db')
# SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True


#Cache Configuration
CACHE_TYPE = 'simple'

