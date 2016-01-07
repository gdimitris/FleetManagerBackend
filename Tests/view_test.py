import unittest
from Application import app, db


class ViewTests(unittest.TestCase):

    def setUp(self):
        app.config.from_pyfile('../Tests/testing_conf.py')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

