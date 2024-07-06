from .base_test import BaseResourcesTest


class TestBaseHangman(BaseResourcesTest):

    def setUp(self):
        super().setUp()

        self.hangman_mock = self.mocks.get('hangman_mock')
        self.logger_mock = self.mocks.get('logger_mock')

    def get_url(self):
        return '/api/games/hangman'


class TestStart(TestBaseHangman):

    # create a new game as guest if cookies are not given
    # create a new game with player data if cookies are there and are valid
    # return 500 if there was an issue while creating the game
    # return game data if creation is successfully

    def test_call_hangman_handler(self):
        self.app.post(self.get_url())
        self.hangman_mock.create_game.assert_called_once()

    def test_return_create_game_result_as_request_data(self):
        self.hangman_mock.create_game.return_value = {
            "game_id": self.fake.random_number(),
            "masked_word": "_____",
            "remaining_attempts": self.fake.random_number()
        }

        response = self.app.post(self.get_url())
        self.assertEqual(response.get_json(), self.hangman_mock.create_game.return_value)

    def test_return_500_if_there_are_errors_while_creating_game(self):
        self.hangman_mock.create_game.side_effect = Exception('foo')
        response = self.app.post(self.get_url())
        self.assertEqual(response.status_code, 500)
