from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.serializers import ScoreSerializer


# Create your tests here.
class ProjectTests(APITestCase):
    fixtures = ["score", "user", "gametype"]

    def test_return_all_scores(self):
        url = reverse("score-list")

        response = self.client.get(url, format="json")
        has_records = len(response.data) > 0
        serializer = ScoreSerializer(data=response.data, many=True)
        self.assertTrue(serializer.is_valid())
        self.assertTrue(has_records)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_return_score_for_game_type(self):
        url = reverse("score-list")
        test_game_filter = {"filter": "test-game"}
        hangman_game_filter = {"filter": "hangman"}

        test_response = self.client.get(f"{url}", test_game_filter, format="json")
        hangman_response = self.client.get(f"{url}", hangman_game_filter, format="json")

        for hangman_score in hangman_response.data:
            self.assertEqual(hangman_score.get("game"), "hangman")

        for test_score in test_response.data:
            self.assertEqual(test_score.get("game"), "testgame")
