import unittest
from unittest.mock import Mock
from src.domain.handlers import AuthHandler
from faker import Faker


class TestAuthHandler(unittest.TestCase):
    def setUp(self):
        self.logger = Mock()
        self.oauth_service = Mock()
        self.user_service = Mock()
        self.fake = Faker()

        self.handler = AuthHandler(
            logger=self.logger,
            oauth_service=self.oauth_service,
            user_service=self.user_service
        )

    def test_handle_login_request(self):
        self.handler.handle_login_request()
        self.oauth_service.send_authorization_request.assert_called_once_with(flask_url='auth.Authorize')

    def test_handle_authorization_callback(self):
        mock_token_info = self.oauth_service.retrieve_authorization_token.return_value
        dummy_user_from_oauth = {
            'email': self.fake.email(),
            'given_name': self.fake.name()
        }
        self.oauth_service.get_user_info.return_value = dummy_user_from_oauth

        dummy_user_data = {
            'email': dummy_user_from_oauth['email'],
            'name': dummy_user_from_oauth['given_name'],
        }

        mock_user_on_db = self.user_service.create_user.return_value

        token_info, user_on_db = self.handler.handle_authorization_callback()

        self.oauth_service.retrieve_authorization_token.assert_called_once()
        self.oauth_service.store_token_info_in_session.assert_called_once_with(token_info=mock_token_info)
        self.oauth_service.get_user_info.assert_called_once()
        self.user_service.create_user.assert_called_once_with(user_data=dummy_user_data)

        self.assertEqual(token_info, mock_token_info)
        self.assertEqual(user_on_db, mock_user_on_db)

    def test_logout(self):
        self.handler.handle_logout_request()
        self.oauth_service.log_user_out.assert_called_once()

if __name__ == "__main__":
    unittest.main()
