from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


# Create your tests here.
class HealthCheckTests(APITestCase):
    def test_get(self):
        url = reverse("health")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
