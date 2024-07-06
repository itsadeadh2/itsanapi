import unittest
from unittest.mock import Mock
from src.domain.handlers import ContactHandler
from src.infrastructure.exc import PersistenceError, QueueInteractionError, DbLookupError
from faker import Faker


class TestBaseContactHandler(unittest.TestCase):
    def setUp(self):
        self.validators = Mock()
        self.email = Mock()
        self.queue = Mock()
        self.handler = ContactHandler(
            email=self.email,
            queue=self.queue
        )
        self.fake = Faker()


class TestContactHandlerPost(TestBaseContactHandler):

    def test_success(self):
        event = {'email': self.fake.email()}
        self.handler.handle_post(data=event)
        self.email.save.assert_called_once_with(event['email'])
        self.queue.add_to_queue.assert_called_once_with(event['email'])


class TestContactHandlerGet(TestBaseContactHandler):
    def test_success(self):
        result = self.handler.handle_get()
        self.assertEqual(result, self.email.query.return_value)


if __name__ == "__main__":
    unittest.main()
