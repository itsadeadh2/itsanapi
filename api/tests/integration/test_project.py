from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.serializers.project import ProjectSerializer


# Create your tests here.
class ProjectTests(APITestCase):
    fixtures = ["project"]

    def test_get(self):
        url = reverse("project-list")

        response = self.client.get(url, format="json")
        has_records = len(response.data) > 0
        serializer = ProjectSerializer(data=response.data, many=True)
        self.assertTrue(serializer.is_valid())
        self.assertTrue(has_records)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
