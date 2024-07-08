import unittest
from unittest.mock import Mock, patch

from faker import Faker

from src.infrastructure.services import ContactRequestService


class TestContactRequestService(unittest.TestCase):

    def setUp(self):
        self.db = Mock()
        self.faker = Faker()
        self.service = ContactRequestService(db=self.db)

    def test_init_success(self):
        raised = False
        try:
            ContactRequestService(db=self.db)
        except Exception:
            raised = True

        self.assertEqual(False, raised)

    def test_init_failure(self):
        with self.assertRaises(Exception):
            ContactRequestService()


class TestCreateContactRequest(TestContactRequestService):

    @patch('src.infrastructure.services.contact_request_service.ContactRequestsModel')
    def test_create_contact_request(self, contact_requests_model):
        email = self.faker.email()

        result = self.service.create_contact_request(email=email)

        contact_requests_model.assert_called_once_with(email=email)
        self.db.session.add.assert_called_once_with(contact_requests_model.return_value)
        self.db.session.commit.assert_called_once()
        self.assertEqual(result, contact_requests_model.return_value)


class TestGetAllContactRequests(TestContactRequestService):

    @patch('src.infrastructure.services.contact_request_service.ContactRequestsModel')
    def test_get_all_contact_requests(self, contact_requests_model):
        res = self.service.get_all_contact_requests()
        contact_requests_model.query.all.assert_called_once()
        self.assertEqual(res, contact_requests_model.query.all.return_value)
