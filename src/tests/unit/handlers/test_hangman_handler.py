import unittest
from unittest.mock import Mock

from faker import Faker

from src.domain.handlers import HangmanHandler


class TestHangmanHandler(unittest.TestCase):

    def setUp(self):
        self.faker = Faker()
        self.hangman_service = Mock()
        self.user_service = Mock()
        self.handler = HangmanHandler(
            hangman_service=self.hangman_service, user_service=self.user_service
        )

    def test_init_success(self):
        raised = False
        try:
            HangmanHandler(
                hangman_service=self.hangman_service, user_service=self.user_service
            )
        except Exception:
            raised = True

        self.assertEqual(False, raised)

    def test_init_failure(self):
        with self.assertRaises(Exception):
            HangmanHandler()

    def test_create_game(self):
        res = self.handler.create_game()
        self.user_service.get_user_from_token.assert_called_once()
        self.hangman_service.create_game.assert_called_once_with(
            user_id=self.user_service.get_user_from_token.return_value.id
        )
        self.assertEqual(res, self.hangman_service.create_game.return_value)

    def test_get_game(self):
        game_id = self.faker.random_number()

        res = self.handler.get_game(game_id=game_id)

        self.user_service.get_user_from_token.assert_called_once()
        self.hangman_service.get_game.assert_called_once_with(
            game_id=game_id,
            user_id=self.user_service.get_user_from_token.return_value.id,
        )
        self.assertEqual(res, self.hangman_service.get_game.return_value)

    def test_take_guess(self):
        guess = self.faker.random_letter()
        game_id = self.faker.random_number()
        self.handler.get_game = Mock()

        res = self.handler.take_guess(guess=guess, game_id=game_id)

        self.handler.get_game.assert_called_once_with(game_id=game_id)
        self.hangman_service.take_guess.assert_called_once_with(
            guess=guess, game=self.handler.get_game.return_value
        )
        self.assertEqual(res, self.hangman_service.take_guess.return_value)

    def test_get_all_games(self):
        res = self.handler.get_all_games()
        self.user_service.get_user_from_token.assert_called_once()
        self.hangman_service.get_all_games.assert_called_once_with(
            user_id=self.user_service.get_user_from_token.return_value.id
        )
        self.assertEqual(res, self.hangman_service.get_all_games.return_value)

    def test_get_leaderboard(self):
        res = self.handler.get_leaderboard()
        self.assertEqual(res, self.hangman_service.get_leaderboard.return_value)
