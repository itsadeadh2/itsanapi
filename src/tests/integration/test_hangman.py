from src.infrastructure.exc import GameOver
from src.tests.integration.base_test import BaseTest
from src.infrastructure.schemas import HangmanGameSchema
from faker import Faker
from unittest.mock import patch


class BaseHangmanTest(BaseTest):
    def setUp(self):
        super().setUp()
        _, access_token = self.create_user()
        self.access_token = access_token

    def create_user(self):
        user_data = {
            'name': Faker().name(),
            'email': Faker().email(),
            'password': Faker().password()
        }
        login = {
            'email': user_data.get('email'),
            'password': user_data.get('password')
        }
        self.app.post('/api/user/register', json=user_data)
        res = self.app.post('/api/user/login', json=login)
        data = res.get_json()
        access_token = data.get('access_token')
        return user_data, access_token

    def create_game(self, access_token=None):
        return self.app.post(
            '/api/games/hangman',
            headers={
                'Authorization': f'Bearer {access_token or self.access_token}'
            }
        )


class TestCreateGame(BaseHangmanTest):

    def test_return_new_game(self):
        res = self.create_game()
        response_data = res.get_json()
        # Schema.validate will return a dict containing errors
        # so if the dict is empty it means the data is valid
        return_data_valid = True if not HangmanGameSchema().validate(response_data) else False
        self.assertEqual(res.status_code, 201)
        self.assertEqual(return_data_valid, True)

    def test_require_auth(self):
        res = self.app.post(
            '/api/games/hangman'
        )
        self.assertEqual(res.status_code, 401)

    @patch('src.setup.injector.HangmanHandler')
    def test_return_500_on_error(self, hangman_handler_mock):
        handler_instance_mock = hangman_handler_mock.return_value
        handler_instance_mock.create_game.side_effect = Exception('foo')
        res = self.create_game()
        self.assertEqual(res.status_code, 500)


class TestGetAllGames(BaseHangmanTest):

    @patch('src.setup.injector.HangmanHandler')
    def test_return_500_on_error(self, hangman_handler_mock):
        handler_instance_mock = hangman_handler_mock.return_value
        handler_instance_mock.get_all_games.side_effect = Exception('foo')
        res = self.app.get(
            '/api/games/hangman',
            headers={
                'Authorization': f'Bearer {self.access_token}'
            }
        )
        self.assertEqual(res.status_code, 500)

    def test_require_auth(self):
        res = self.app.get(
            '/api/games/hangman',
        )
        self.assertEqual(res.status_code, 401)

    def test_return_all_games_from_user(self):
        # create games for user 1
        _, user1_access_token = self.create_user()
        user1_total_games = Faker().random_int(min=1, max=10)
        for _ in range(user1_total_games):
            self.create_game(access_token=user1_access_token)

        # call setup to generate a new user
        self.setUp()
        # create games for user 2
        _, user2_access_token = self.create_user()
        user2_total_games = Faker().random_int(min=1, max=10)
        for _ in range(user2_total_games):
            self.create_game(access_token=user2_access_token)

        user1_res = self.app.get(
            '/api/games/hangman',
            headers={
                'Authorization': f'Bearer {user1_access_token}'
            }
        )
        user2_res = self.app.get(
            '/api/games/hangman',
            headers={
                'Authorization': f'Bearer {user2_access_token}'
            }
        )
        user1_res_data = user1_res.get_json()
        user2_res_data = user2_res.get_json()

        self.assertEqual(len(user1_res_data), user1_total_games)
        self.assertEqual(len(user2_res_data), user2_total_games)


class TestGetGame(BaseHangmanTest):

    def setUp(self):
        super().setUp()
        res = self.app.post(
            '/api/games/hangman',
            headers={
                'Authorization': f'Bearer {self.access_token}'
            }
        )
        res_data = res.get_json()
        self.game_id = res_data.get('id')

    def test_return_game(self):
        res = self.app.get(
            f'/api/games/hangman/{self.game_id}',
            headers={
                'Authorization': f'Bearer {self.access_token}'
            }
        )
        response_data = res.get_json()
        # Schema.validate will return a dict containing errors
        # so if the dict is empty it means the data is valid
        return_data_valid = True if not HangmanGameSchema().validate(response_data) else False
        self.assertEqual(res.status_code, 200)
        self.assertEqual(return_data_valid, True)

    def test_require_auth(self):
        res = self.app.get(
            f'/api/games/hangman/{self.game_id}',
        )
        self.assertEqual(res.status_code, 401)

    @patch('src.setup.injector.HangmanHandler')
    def test_return_500_on_error(self, hangman_handler_mock):
        # hangman handler is created in the injector
        # call setup in here again so that the app is recreated
        # with a mock instance
        self.setUp()
        handler_instance_mock = hangman_handler_mock.return_value
        handler_instance_mock.get_game.side_effect = Exception('foo')
        res = self.app.get(
            f'/api/games/hangman/{self.game_id}',
            headers={
                'Authorization': f'Bearer {self.access_token}'
            }
        )
        self.assertEqual(res.status_code, 500)

    def test_return_404_on_error(self):
        res = self.app.get(
            f'/api/games/hangman/{Faker().random_number()}',
            headers={
                'Authorization': f'Bearer {self.access_token}'
            }
        )
        self.assertEqual(res.status_code, 404)


class TestTakeGuess(BaseHangmanTest):

    def setUp(self):
        super().setUp()
        res = self.create_game()
        self.game_id = res.get_json().get('id')

    def take_guess(self, game_id, guess: dict):
        return self.app.post(
            f'/api/games/hangman/{game_id}/guess',
            headers={
                'Authorization': f'Bearer {self.access_token}'
            },
            json=guess
        )

    def test_return_422_if_guess_is_invalid(self):
        guess = {
            'guess': 'morethanoneletter'
        }
        res = self.take_guess(game_id=self.game_id, guess=guess)
        self.assertEqual(res.status_code, 422)

    def test_return_game_state_after_guess(self):
        guess = {
            'guess': Faker().random_letter()
        }
        res = self.take_guess(game_id=self.game_id, guess=guess)
        self.assertEqual(res.status_code, 200)

        is_game_data_valid = True if not HangmanGameSchema().validate(res.get_json()) else False
        self.assertEqual(True, is_game_data_valid)

    @patch('src.setup.injector.HangmanHandler')
    def test_return_400_if_game_is_over(self, hangman_handler_mock):
        self.setUp()
        hangman_instance = hangman_handler_mock.return_value
        hangman_instance.take_guess.side_effect = GameOver()
        # game will be over after 6 guesses
        guess = {
            'guess': Faker().random_letter()
        }
        res = self.take_guess(game_id=self.game_id, guess=guess)
        self.assertEqual(res.status_code, 400)


class TestGetLeaderboard(BaseHangmanTest):
    @patch('src.setup.injector.HangmanHandler')
    def test_return_500_on_error(self, hangman_handler_mock):
        hangman_instance = hangman_handler_mock.return_value
        hangman_instance.get_leaderboard.side_effect = Exception()
        res = self.app.get('/api/games/hangman/leaderboard')
        self.assertEqual(res.status_code, 500)

    def test_return_entries_for_current_users(self):
        amount_of_users = Faker().random_int(min=10, max=20)
        for _ in range(amount_of_users):
            self.create_user()

        res = self.app.get('/api/games/hangman/leaderboard')
        res_data = res.get_json()

        self.assertEqual(True, len(res_data) >= amount_of_users)
