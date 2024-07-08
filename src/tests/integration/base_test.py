import os
from unittest import TestCase

from flask_migrate import upgrade

from src.app import create_app
from src.database.db import db


class BaseTest(TestCase):
    TEST_DATABASE_URI = "sqlite:///test.db"

    def setUp(self):
        os.environ['DATABASE_URL'] = self.TEST_DATABASE_URI
        app = create_app()
        self.app = app.test_client()
        self.app_context = app.app_context()

        with self.app_context:
            # Create all tables and apply migrations
            db.create_all()

    def tearDown(self):
        with self.app_context:
            # Drop all tables
            db.drop_all()
