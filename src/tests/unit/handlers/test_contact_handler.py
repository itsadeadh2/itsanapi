import unittest
from unittest.mock import Mock

from faker import Faker

from src.domain.handlers import ContactHandler


class TestContactHandler(unittest.TestCase):

    def setUp(self):
        self.faker = Faker()
        self.cr_service = Mock()
        self.queue_service = Mock()
        self.handler = ContactHandler(
            contact_request_service=self.cr_service, queue_service=self.queue_service
        )

    def test_init_success(self):
        raised = False
        try:
            self.handler = ContactHandler(
                contact_request_service=self.cr_service,
                queue_service=self.queue_service,
            )
        except Exception:
            raised = True

        self.assertEqual(False, raised)

    def test_init_failure(self):
        with self.assertRaises(Exception):
            ContactHandler()

    def test_handle_post(self):
        data = {"email": self.faker.email()}

        res = self.handler.handle_post(data=data)

        self.cr_service.create_contact_request.assert_called_once_with(
            email=data.get("email")
        )
        self.queue_service.add_to_queue.assert_called_once_with(data.get("email"))
        self.assertEqual(True, type(res) is dict)

    def test_handle_get(self):
        self.handler.handle_get()
        self.cr_service.get_all_contact_requests.assert_called_once()
