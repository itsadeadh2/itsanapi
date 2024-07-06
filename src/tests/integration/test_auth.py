from unittest.mock import Mock
from unittest import TestCase
from faker import Faker
from flask_injector import FlaskInjector
from injector import Module, provider, singleton
from src.domain.handlers import AuthHandler
from src.app import create_app
from logging import Logger


class BaseTestAuth(TestCase):

    def setUp(self):
        auth_mock = Mock()
        logger_mock = Mock()

        class MockInjector(Module):
            @singleton
            @provider
            def provide_auth_handler(self) -> AuthHandler:
                return auth_mock

            @singleton
            @provider
            def provide_logger(self) -> Logger:
                return logger_mock

        self.auth_mock = auth_mock
        self.logger_mock = logger_mock

        app = create_app()
        FlaskInjector(app=app, modules=[MockInjector])
        self.app = app.test_client()
        self.fake = Faker()


class TestAuthLogin(BaseTestAuth):

    def test_call_handler(self):
        fake_response = {}, 200
        self.auth_mock.handle_login_request.return_value = fake_response
        res = self.app.get('/login')
        self.auth_mock.handle_login_request.assert_called_once()
        self.assertEqual(res.status_code, 200)

    def test_return_500_if_exception_is_raised(self):
        self.auth_mock.handle_login_request.side_effect = Exception('foo')
        res = self.app.get('/login')
        self.auth_mock.handle_login_request.assert_called_once()
        self.assertEqual(res.status_code, 500)


class TestLoginAuthorize(BaseTestAuth):
    def test_call_handler(self):
        dummy_token_info = {
            'access_token': '',
            'expires_at': ''
        }
        dummy_user = {}
        self.auth_mock.handle_authorization_callback.return_value = dummy_token_info, dummy_user
        res = self.app.get('/login/authorize')
        self.auth_mock.handle_authorization_callback.assert_called_once()
        self.assertEqual(res.status_code, 302)


class TestLogout(BaseTestAuth):

    def test_call_handler(self):
        res = self.app.get('/logout')
        self.auth_mock.handle_logout_request.assert_called_once()
        self.assertEqual(res.status_code, 302)
