import os
import unittest

from views import app, db
from _config import basedir
from models import User


TEST_DB = 'test.db'


class UserTests(unittest.TestCase):
    # setup
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()
