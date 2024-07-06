from unittest.mock import Mock
from unittest import TestCase
from faker import Faker
from flask_injector import FlaskInjector
from injector import Module, provider, singleton
from src.domain.handlers import ContactHandler
from src.app import create_app
from logging import Logger
from src.infrastructure.exc import DbLookupError, InvalidEmailError, PersistenceError, QueueInteractionError


class BaseTestContact(TestCase):

    def setUp(self):
        contact_mock = Mock()
        logger_mock = Mock()

        class MockInjector(Module):
            @singleton
            @provider
            def provide_contact_handler(self) -> ContactHandler:
                return contact_mock

            @singleton
            @provider
            def provide_logger(self) -> Logger:
                return logger_mock

        self.contact_mock = contact_mock
        self.logger_mock = logger_mock

        app = create_app()
        FlaskInjector(app=app, modules=[MockInjector])
        self.app = app.test_client()
        self.fake = Faker()


class TestContactPost(BaseTestContact):

    def test_call_post_with_email_data(self):
        email_data = {
            'email': self.fake.email()
        }
        fake_response = []
        self.contact_mock.handle_post.return_value = fake_response
        res = self.app.post('/api/contact', json=email_data)
        self.contact_mock.handle_post.assert_called_once_with(email_data)
        self.assertEqual(res.status_code, 200)

    def test_return_500_if_exception_is_raised(self):
        email_data = {
            'email': self.fake.email()
        }
        self.contact_mock.handle_post.side_effect = Exception('foo')
        res = self.app.post('/api/contact', json=email_data)
        self.assertEqual(res.status_code, 500)

    def test_return_400_if_invalid_exception_is_raised(self):
        email_data = {
            'email': self.fake.email()
        }
        self.contact_mock.handle_post.side_effect = InvalidEmailError('foo')
        res = self.app.post('/api/contact', json=email_data)
        self.assertEqual(res.status_code, 400)

    def test_return_500_if_persistence_error_is_raised(self):
        email_data = {
            'email': self.fake.email()
        }
        self.contact_mock.handle_post.side_effect = PersistenceError('foo')
        res = self.app.post('/api/contact', json=email_data)
        self.assertEqual(res.status_code, 500)

    def test_return_500_if_queue_error_is_raised(self):
        email_data = {
            'email': self.fake.email()
        }
        self.contact_mock.handle_post.side_effect = QueueInteractionError('foo')
        res = self.app.post('/api/contact', json=email_data)
        self.assertEqual(res.status_code, 500)


class TestContactGet(BaseTestContact):

    def test_call_get_return_200(self):
        fake_response = []
        self.contact_mock.handle_get.return_value = fake_response
        res = self.app.get('/api/contact')
        self.contact_mock.handle_get.assert_called_once()
        self.assertEqual(res.status_code, 200)

    def test_return_500_if_exception_is_raised(self):
        self.contact_mock.handle_get.side_effect = Exception('foo')
        res = self.app.get('/api/contact')
        self.contact_mock.handle_get.assert_called_once()
        self.assertEqual(res.status_code, 500)

    def test_return_500_if_db_lookup_is_raised(self):
        self.contact_mock.handle_get.side_effect = DbLookupError('foo')
        res = self.app.get('/api/contact')
        self.contact_mock.handle_get.assert_called_once()
        self.assertEqual(res.status_code, 500)