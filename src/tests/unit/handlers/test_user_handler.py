import unittest
from unittest.mock import Mock

from faker import Faker

from src.domain.handlers import UserHandler


class TestContactHandler(unittest.TestCase):

    def setUp(self):
        self.faker = Faker()
        self.user_service = Mock()
        self.hangman_service = Mock()
        self.handler = UserHandler(
            user_service=self.user_service, hangman_service=self.hangman_service
        )
        self.user_data = {
            "name": self.faker.name(),
            "email": self.faker.email(),
            "password": self.faker.password(),
        }

    def test_init_success(self):
        raised = False
        try:
            self.handler = UserHandler(
                user_service=self.user_service, hangman_service=self.hangman_service
            )
        except Exception:
            raised = True

        self.assertEqual(False, raised)

    def test_init_failure(self):
        with self.assertRaises(Exception):
            UserHandler()

    def test_create_user(self):
        self.handler.create_user(user_data=self.user_data)
        self.user_service.create_user.assert_called_once_with(self.user_data)
        self.hangman_service.get_or_create_score.assert_called_once_with(
            user_id=self.user_service.create_user.return_value.id
        )

    def test_login_user(self):
        self.handler.log_in_user(user_data=self.user_data)
        self.user_service.log_in_user.assert_called_once_with(user_data=self.user_data)

    def test_logout_user(self):
        self.handler.log_out_user()
        self.user_service.log_out_user.assert_called_once()
