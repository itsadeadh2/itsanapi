import unittest
from unittest.mock import Mock, patch

from faker import Faker

from src.infrastructure.exc import UserAlreadyExists, InvalidCredentials
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


class TestCreateUser(TestHangmanService):

    @patch("src.infrastructure.services.user_service.UserModel")
    def test_raises_if_user_already_exists(self, _):
        user_data = {"email": self.faker.email()}
        with self.assertRaises(UserAlreadyExists):
            self.service.create_user(user_data=user_data)

    @patch("src.infrastructure.services.user_service.UserModel")
    @patch("src.infrastructure.services.user_service.pbkdf2_sha256")
    def test_create_user(self, pbk_mock, user_model_mock):
        user_data = {
            "email": self.faker.email(),
            "password": self.faker.password(),
            "name": self.faker.name(),
        }
        user_model_mock.query.filter().first.return_value = None

        created_user = self.service.create_user(user_data=user_data)

        user_model_mock.assert_called_once_with(
            name=user_data["name"],
            email=user_data["email"],
            password=pbk_mock.hash.return_value,
        )
        self.db.session.add.assert_called_once_with(created_user)
        self.db.session.commit.assert_called_once()
        self.assertEqual(created_user, user_model_mock.return_value)


class TestLogInUser(TestHangmanService):
    def test_raises_invalid_credentials(self):
        user_data = {"email": self.faker.email(), "password": self.faker.password()}

        self.service.get_user_by_email = Mock()
        self.service.get_user_by_email.side_effect = Exception("dummy")

        with self.assertRaises(InvalidCredentials):
            self.service.log_in_user(user_data=user_data)

    def test_raises_if_no_user_and_password_match(self):
        user_data = {"email": self.faker.email(), "password": self.faker.password()}
        self.service.get_user_by_email = Mock()
        self.service.check_user_password = Mock()
        self.service.check_user_password.return_value = False
        self.service.create_token = Mock()

        with self.assertRaises(InvalidCredentials):
            self.service.log_in_user(user_data=user_data)

    def test_return_token(self):
        user_data = {"email": self.faker.email(), "password": self.faker.password()}
        self.service.get_user_by_email = Mock()
        self.service.check_user_password = Mock()
        self.service.create_token = Mock()

        result = self.service.log_in_user(user_data=user_data)

        self.service.get_user_by_email.assert_called_once_with(user_data.get("email"))
        self.service.check_user_password.assert_called_once_with(
            given_password=user_data.get("password"),
            encrypted_password=self.service.get_user_by_email.return_value.password,
        )
        self.service.create_token.assert_called_once_with(
            user_id=self.service.get_user_by_email.return_value.id
        )
        self.assertEqual(result, self.service.create_token.return_value)


class TestLogOutUser(TestHangmanService):
    @patch("src.infrastructure.services.user_service.ExpiredTokensModel")
    @patch("src.infrastructure.services.user_service.get_jwt")
    def test_logout_user(self, get_jwt_mock, expired_tokens_model_mock):
        jwt = {"jti": self.faker.random_number()}

        get_jwt_mock.return_value = jwt

        self.service.log_out_user()
        get_jwt_mock.assert_called_once()
        expired_tokens_model_mock.assert_called_once_with(jti=jwt["jti"])
        self.db.session.add.assert_called_once_with(
            expired_tokens_model_mock.return_value
        )
        self.db.session.commit.assert_called_once()


class TestGetUserByEmail(TestHangmanService):
    @patch("src.infrastructure.services.user_service.UserModel")
    def test_get_user_by_email(self, user_model_mock):
        email = self.faker.email()

        result = self.service.get_user_by_email(email=email)

        user_model_mock.query.filter().first.assert_called_once()
        self.assertEqual(result, user_model_mock.query.filter().first.return_value)


class TestGetUserFromToken(TestHangmanService):
    @patch("src.infrastructure.services.user_service.UserModel")
    @patch("src.infrastructure.services.user_service.get_jwt_identity")
    def test_get_user_from_token(self, get_jwt_mock, user_model_mock):
        result = self.service.get_user_from_token()

        get_jwt_mock.assert_called_once()
        user_model_mock.query.get_or_404.assert_called_once_with(
            get_jwt_mock.return_value
        )
        self.assertEqual(result, user_model_mock.query.get_or_404.return_value)


class TestCheckUserPassword(TestHangmanService):
    @patch("src.infrastructure.services.user_service.pbkdf2_sha256")
    def test_check_user_password(self, pbk_mock):
        given_password = self.faker.password()
        encrypted_password = self.faker.password()
        result = self.service.check_user_password(given_password, encrypted_password)
        pbk_mock.verify.assert_called_once_with(given_password, encrypted_password)
        self.assertEqual(result, pbk_mock.verify.return_value)


class CreateToken(TestHangmanService):

    @patch("src.infrastructure.services.user_service.create_access_token")
    def test_create_token(self, create_access_token_mock):
        user_id = self.faker.random_number()
        result = self.service.create_token(user_id=user_id)
        create_access_token_mock.assert_called_once_with(identity=user_id)
        self.assertEqual(result, create_access_token_mock.return_value)
