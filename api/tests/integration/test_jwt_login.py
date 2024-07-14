from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase


# Create your tests here.
class JWTLoginTests(APITestCase):
    fixtures = ["user", "gametype"]

    def setUp(self):
        self.faker = Faker()

        self.user_data = {"email": self.faker.email(), "password": self.faker.password()}
        User = get_user_model()
        self.user = User(**self.user_data)
        self.user.set_password(self.user_data.get('password'))
        self.user.save()

    def test_login_failure(self):
        url = reverse("token_obtain_pair")
        data = {"email": self.user.email, "password": self.faker.password()}

        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_success(self):
        url = reverse("token_obtain_pair")
        data = {"email": self.user.email, "password": self.user_data.get("password")}

        response = self.client.post(url, data=data, format="json")
        access_token = response.json().get('access')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(access_token)

        hangman_url = reverse("hangman-list")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        response = self.client.post(hangman_url, data=None, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
