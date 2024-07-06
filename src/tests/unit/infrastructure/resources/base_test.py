from unittest.mock import Mock
from unittest import TestCase
from faker import Faker
from flask_injector import FlaskInjector
from injector import Module, provider, singleton
from src.domain.handlers import AuthHandler, ContactHandler, HangmanHandler
from src.app import create_app
from logging import Logger


class BaseResourcesTest(TestCase):

    def setUp(self):
        logger_mock = Mock()
        auth_mock = Mock()
        contact_mock = Mock()
        hangman_mock = Mock()

        class MockInjector(Module):

            @singleton
            @provider
            def provide_logger(self) -> Logger:
                return logger_mock

            @singleton
            @provider
            def provide_auth_handler(self) -> AuthHandler:
                return auth_mock

            @singleton
            @provider
            def provide_contact_handler(self) -> ContactHandler:
                return contact_mock

            @singleton
            @provider
            def provide_hangman_service(self) -> HangmanHandler:
                return hangman_mock

        self.mocks = {
            'auth_mock': auth_mock,
            'logger_mock': logger_mock,
            'contact_mock': contact_mock,
            'hangman_mock': hangman_mock
        }

        app = create_app()
        FlaskInjector(app=app, modules=[MockInjector])
        self.app = app.test_client()
        self.fake = Faker()
