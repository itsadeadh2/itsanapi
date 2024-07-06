from src.infrastructure.exc import DbLookupError, InvalidEmailError, PersistenceError, QueueInteractionError
from .base_test import BaseResourcesTest


class BaseTestContact(BaseResourcesTest):

    def setUp(self):
        super().setUp()

        self.contact_mock = self.mocks.get('contact_mock')
        self.logger_mock = self.mocks.get('logger_mock')


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
