from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from api.views.contact_request import CreateContactRequestView


class ContactTests(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_raise_error_on_invalid_email(self):
        url = reverse("contact")
        invalid_emails = ["invalidmail", "invalid@mail", "@invalid.com"]
        for email in invalid_emails:
            data = {"email": email}
            response = self.client.post(url, data, format="json")
            response_data = response.json()
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual("email" in response_data, True)

    @patch("api.views.contact_request.QueueService")
    def test_send_email(self, queue_mock):
        queue_instance = queue_mock.return_value
        view = CreateContactRequestView.as_view()
        data = {"email": "itsadeadh2@gmail.com"}
        request = self.factory.post("/contacts", data=data, format="json")
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("email"), data.get("email"))
        queue_instance.add_to_queue.assert_called_once_with(email=data.get("email"))
