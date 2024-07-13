from django.contrib.auth.models import User
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import HangmanGame


# Create your tests here.
class BaseHangman(APITestCase):
    fixtures = ["user", "gametype"]

    def setUp(self):
        self.faker = Faker()
        self.user = User.objects.get(id=1)


class HangmanTests(BaseHangman):
    def test_fails_to_create_if_not_authenticated(self):
        url = reverse("hangman-list")

        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_game_if_authenticated(self):
        url = reverse("hangman-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, format="json")
        created_game = HangmanGame.objects.get(id=response.data.get("id"))
        self.assertEqual(created_game.status, HangmanGame.Status.IN_PROGRESS)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fails_to_retrieve_if_not_authenticated(self):
        url = reverse("hangman-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_games_if_authenticated(self):
        url = reverse("hangman-list")
        self.client.force_authenticate(user=self.user)
        self.client.post(url, format="json")
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class HangmanGuessTests(BaseHangman):
    def setUp(self):
        super().setUp()
        url = reverse("hangman-list")

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, format="json")
        self.game = HangmanGame.objects.get(id=response.data.get("id"))

    def test_fails_to_guess_if_not_authenticated(self):
        url = reverse("hangman-guess", kwargs={"pk": self.game.id})
        self.client.force_authenticate(user=None)
        data = {"guess": "a"}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_fails_to_guess_if_guess_is_invalid(self):
        url = reverse("hangman-guess", kwargs={"pk": self.game.id})
        data = {"guess": "invalidguess"}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("guess" in response.json())

        data = {"guess": ""}
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("guess" in response.json())

    def test_win_game(self):
        url = reverse("hangman-guess", kwargs={"pk": self.game.id})
        guesses = {guess for guess in self.game.solution}
        for guess in guesses:
            data = {"guess": guess}
            response = self.client.post(url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.game = HangmanGame.objects.get(id=self.game.id)
        self.assertEqual(self.game.status, HangmanGame.Status.WON)

    def test_lose_game(self):
        url = reverse("hangman-guess", kwargs={"pk": self.game.id})

        self.game.solution = "fakesolution"
        self.game.masked_word = HangmanGame.get_masked_text(self.game.solution)
        self.game.save()
        wrong_guesses = "xvphmz"

        for wrong_guess in list(wrong_guesses):
            data = {"guess": wrong_guess}
            response = self.client.post(url, data=data, format="json")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.game = HangmanGame.objects.get(id=self.game.id)
        self.assertEqual(self.game.status, HangmanGame.Status.LOST)
