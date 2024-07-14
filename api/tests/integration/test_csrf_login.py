from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient


class CSRFLoginTests(APITestCase):
    fixtures = ["user", "gametype"]

    def setUp(self):
        self.faker = Faker()

        self.client = APIClient(enforce_csrf_checks=True)

        self.user_data = {"email": self.faker.email(), "password": self.faker.password()}
        User = get_user_model()
        self.user = User(**self.user_data)
        self.user.set_password(self.user_data.get('password'))
        self.user.save()

        self.url = reverse('login-csrf')

    def get_csrf(self):
        response = self.client.get(self.url, format="json")
        return response.cookies.get('csrftoken')

    def test_login_return_csrf_on_get(self):
        csrf = self.get_csrf()
        self.assertIsNotNone(csrf)

    def test_login_failure_if_no_csrf_is_given(self):
        data = {
            "email": self.user.email,
            "password": self.user_data.get("password")
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_login_success(self):
        data = {
            "email": self.user.email,
            "password": self.user_data.get("password")
        }
        csrf = self.get_csrf().value
        self.client.credentials(HTTP_X_CSRFTOKEN=csrf)
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_failure_on_wrong_credentials(self):
        data = {
            "email": self.user.email,
            "password": self.faker.password()
        }
        csrf = self.get_csrf().value
        self.client.credentials(HTTP_X_CSRFTOKEN=csrf)
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
