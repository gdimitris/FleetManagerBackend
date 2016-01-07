import os
import unittest

from config import basedir
from Application import app, db
from Application.models import Researchers

class DBOperationsTests(unittest.TestCase):
    def setUp(self):
        app.config.from_pyfile('../Tests/testing_conf.py')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()


