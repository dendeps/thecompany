"""
This module defines the BaseTestCase class
"""
import unittest

from config import TestingConfig
from thecompany_app import app, db


class BaseTestCase(unittest.TestCase):
    """
    Base test case class
    """

    def setUp(self):
        """
        Execute before every test case
        """
        #self.app = app
        #self.app.config.from_object(TestingConfig)
        #self.app_context = self.app.app_context()
        #self.app_context.push()
        #db.create_all()

        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """
        Execute after every test case
        """
        db.session.remove()
        db.drop_all()