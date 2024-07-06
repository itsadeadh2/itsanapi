import unittest
from unittest.mock import Mock, patch
from faker import Faker

from src.infrastructure.services import UserService
from marshmallow import ValidationError


class BaseUserTest(unittest.TestCase):
    def setUp(self):
        self.fake = Faker()
        self.db = Mock()
        self.logger = Mock()
        self.user_schema = Mock()
        self.user_service = UserService(db=self.db, logger=self.logger, user_schema=self.user_schema)


class TestGetUserByEmail(BaseUserTest):
    @patch('src.infrastructure.services.user.UserModel')
    def test_returns_user_if_exists(self, mock_user_model):
        email = self.fake.email()
        dummy_user = {
            'email': email
        }
        mock_result = Mock()
        mock_result.first.return_value = dummy_user
        mock_user_model.query.filter.return_value = mock_result

        self.user_service.get_user_by_email(email=email)

        self.user_schema.dump.assert_called_once_with(dummy_user)

    @patch('src.infrastructure.services.user.UserModel')
    def test_returns_false_if_user_dont_exist(self, mock_user_model):
        email = self.fake.email()
        mock_result = Mock()
        mock_result.first.return_value = {}
        mock_user_model.query.filter.return_value = mock_result

        result = self.user_service.get_user_by_email(email=email)
        self.assertEqual(result, False)
        self.user_schema.dump.assert_not_called()


class TestCreateUser(unittest.TestCase):
    def setUp(self):
        self.fake = Faker()
        self.db = Mock()
        self.logger = Mock()
        self.user_schema = Mock()
        self.user_service = UserService(db=self.db, logger=self.logger, user_schema=self.user_schema)

    @patch('src.infrastructure.services.user.UserModel')
    def test_return_existing_user_if_already_exists(self, _):
        fake_user = {
            'email': self.fake.email(),
            'name': self.fake.name()
        }
        dummy_user = {
            **fake_user,
            'id': self.fake.random_number()
        }
        self.user_service.get_validated_data = Mock()
        self.user_service.get_validated_data.return_value = fake_user
        self.user_service.get_user_by_email = Mock()
        self.user_service.get_user_by_email.return_value = dummy_user

        result = self.user_service.create_user(fake_user)
        self.assertEqual(result, dummy_user)
        self.user_service.get_validated_data.assert_called_once_with(fake_user)
        self.user_service.get_user_by_email.assert_called_once_with(email=fake_user['email'])

    @patch('src.infrastructure.services.user.UserModel')
    def test_add_user_to_db_if_doesnt_exists(self, _):
        fake_user = {
            'email': self.fake.email(),
            'name': self.fake.name()
        }
        dummy_user = {
            **fake_user,
            'id': self.fake.random_number()
        }
        self.user_service.get_validated_data = Mock()
        self.user_service.get_validated_data.return_value = fake_user
        self.user_service.get_user_by_email = Mock()
        self.user_service.get_user_by_email.return_value = False
        self.user_service.add_user_to_db = Mock()
        self.user_service.add_user_to_db.return_value = dummy_user
        self.user_schema.dump.return_value = dummy_user

        result = self.user_service.create_user(fake_user)
        self.assertEqual(result, dummy_user)
        self.user_service.get_validated_data.assert_called_once_with(fake_user)
        self.user_service.get_user_by_email.assert_called_once_with(email=fake_user['email'])
        self.user_service.add_user_to_db.assert_called_once_with(fake_user)
        self.user_schema.dump.assert_called_once_with(dummy_user)


class TestGetValidatedData(BaseUserTest):
    def test_calls_schema_load(self):
        fake_user = {
            'email': self.fake.email(),
            'name': self.fake.name()
        }
        expected_response = self.user_schema.load.return_value
        result = self.user_service.get_validated_data(user_data=fake_user)
        self.assertEqual(result, expected_response)

    def test_returns_nothing_and_raises_if_data_is_invalid(self):
        fake_user = {
            'email': self.fake.email(),
            'name': self.fake.name()
        }
        self.user_schema.load.side_effect = ValidationError('foo')
        with self.assertRaises(ValidationError):
            self.user_service.get_validated_data(user_data=fake_user)


class TestAddUserToDb(BaseUserTest):

    @patch('src.infrastructure.services.user.UserModel')
    def test_return_new_user_if_no_errors(self, mock_user_model):
        fake_data = {
            'name': self.fake.name(),
            'email': self.fake.email()
        }

        result = self.user_service.add_user_to_db(user_data=fake_data)

        mock_user_model.assert_called_once_with(**fake_data)
        self.db.session.add.assert_called_once_with(mock_user_model.return_value)
        self.db.session.commit.assert_called_once()
        self.assertEqual(result, mock_user_model.return_value)

    @patch('src.infrastructure.services.user.UserModel')
    def test_call_rollback_and_raise_if_error_ocurred(self, mock_user_model):
        fake_data = {
            'name': self.fake.name(),
            'email': self.fake.email()
        }

        self.db.session.add.side_effect = Exception('foo')
        with self.assertRaises(Exception):
            self.user_service.add_user_to_db(user_data=fake_data)
        self.db.session.rollback.assert_called_once()
