import unittest
from unittest.mock import Mock
from src.domain.handlers import HangmanHandler
from faker import Faker
from src.infrastructure.exc import GameCreationError


class TestBaseHangmanHandler(unittest.TestCase):
    def setUp(self):
        self.fake = Faker()
        self.logger = Mock()
        self.oauth_service = Mock()
        self.user_service = Mock()
        self.dao = Mock()

        self.handler = HangmanHandler(
            logger=self.logger,
            oauth_service=self.oauth_service,
            user_service=self.user_service,
            hangman_dao=self.dao
        )

    def test_init_success(self):
        raised = False
        try:
            HangmanHandler(
                logger=self.logger,
                oauth_service=self.oauth_service,
                user_service=self.user_service,
                hangman_dao=self.dao
            )
        except Exception:
            raised = True

        self.assertEqual(raised, False)

    def test_init_failure(self):
        with self.assertRaises(Exception):
            HangmanHandler()


class TestHangmanGetUserEmail(TestBaseHangmanHandler):

    def test_return_user_data_if_exists(self):
        self.oauth_service.get_user_info.return_value = {
            "email": self.fake.email()
        }
        self.user_service.get_user_by_email.return_value = {
            **self.oauth_service.get_user_info.return_value,
            'name': self.fake.name(),
            'id': self.fake.random_number()
        }
        result = self.handler.get_player_data()
        self.assertEqual(result, self.user_service.get_user_by_email.return_value)
        self.user_service.get_user_by_email.assert_called_once_with(
            self.oauth_service.get_user_info.return_value.get('email')
        )

    def test_return_false_if_user_data_doesnt_exist(self):
        self.oauth_service.get_user_info.side_effect = Exception('foo')
        result = self.handler.get_player_data()
        self.assertEqual(result, False)


class TestHangmanCreateGame(TestBaseHangmanHandler):
    def setUp(self):
        super().setUp()
        self.handler.create_user_game = Mock()
        self.handler.create_guest_game = Mock()
        self.handler.get_player_data = Mock()

    def test_create_guest_game_if_no_user(self):
        self.handler.get_player_data.return_value = False
        response = self.handler.create_game()
        self.handler.create_guest_game.assert_called_once()
        self.assertEqual(response, self.handler.create_guest_game.return_value)

    def test_create_user_game_if_user_exists(self):
        self.handler.get_player_data.return_value = {
            'name': self.fake.name(),
            'id': self.fake.random_number(),
            'email': self.fake.email()
        }
        response = self.handler.create_game()
        self.handler.create_user_game.assert_called_once_with(player_data=self.handler.get_player_data.return_value)
        self.assertEqual(response, self.handler.create_user_game.return_value)

    def test_raises_game_error_if_there_are_issues_while_creating(self):
        self.handler.get_player_data.side_effect = Exception('foo')
        with self.assertRaises(GameCreationError):
            self.handler.create_game()


class TestHangmanCreateGuestGame(TestBaseHangmanHandler):
    def test_calls_dao_without_player_data(self):
        result = self.handler.create_guest_game()
        self.dao.create_game.assert_called_once_with()
        self.assertEqual(result, self.dao.create_game.return_value)


class TestHangmanCreatePlayerGame(TestBaseHangmanHandler):

    def test_calls_dao_with_player_data(self):
        fake_data = {
            'name': self.fake.name(),
            'id': self.fake.random_number(),
            'email': self.fake.email()
        }
        result = self.handler.create_user_game(player_data=fake_data)
        self.dao.create_game.assert_called_once_with(player_data=fake_data)
        self.assertEqual(result, self.dao.create_game.return_value)


