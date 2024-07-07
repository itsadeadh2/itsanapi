import unittest
from unittest.mock import Mock

from faker import Faker

from src.infrastructure.services import UserService


class TestHangmanService(unittest.TestCase):
    def setUp(self):
        self.db = Mock()
        self.faker = Faker()
        self.service = UserService(db=self.db)

    def test_init_success(self):
        raised = False
        try:
            UserService(db=self.db)
        except Exception:
            raised = True

        self.assertEqual(False, raised)

    def test_init_failure(self):
        with self.assertRaises(Exception):
            UserService()
