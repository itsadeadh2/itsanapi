from django.contrib.auth import get_user_model
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase


# Create your tests here.
class RegisterTests(APITestCase):
    def setUp(self):
        self.faker = Faker()

    def test_create_user_with_basic_info(self):
        User = get_user_model()
        url = reverse("register")
        data = {"email": self.faker.email(), "password": self.faker.password()}

        response = self.client.post(url, data=data, format="json")
        created_user = User.objects.get(email=data.get("email"))
        self.assertTrue(bool(created_user))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_with_additional_info(self):
        User = get_user_model()
        url = reverse("register")
        data = {
            "password": self.faker.password(),
            "email": self.faker.email(),
            "first_name": self.faker.name(),
            "last_name": self.faker.last_name(),
        }

        response = self.client.post(url, data=data, format="json")
        created_user = User.objects.get(email=data.get("email"))
        self.assertEqual(created_user.email, data["email"])
        self.assertEqual(created_user.first_name, data["first_name"])
        self.assertEqual(created_user.last_name, data["last_name"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
