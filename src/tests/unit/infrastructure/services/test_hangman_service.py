import unittest
from unittest.mock import Mock, patch

from faker import Faker

from src.infrastructure.exc import GameNotFound, GameOver
from src.infrastructure.services import HangmanService
from src.infrastructure.services.hangman_service import GameStatus


class TestHangmanService(unittest.TestCase):
    @patch('src.infrastructure.services.hangman_service.Faker')
    def setUp(self, faker_mock):
        self.db = Mock()
        self.faker_mock = faker_mock
        self.faker = Faker()
        self.service = HangmanService(db=self.db)

    def test_init_success(self):
        raised = False
        try:
            HangmanService(db=self.db)
        except Exception:
            raised = True

        self.assertEqual(False, raised)

    def test_init_failure(self):
        with self.assertRaises(Exception):
            HangmanService()


class TestUtilMethods(TestHangmanService):

    def test_get_masked_text(self):
        word = self.faker.word()
        word_mask = self.service.get_masked_text(word)
        self.assertEqual(len(word_mask), len(word))
        self.assertEqual(True, '_' in word_mask)

    def test_check_valid_guess(self):
        solution = 'foo'
        guess = 'o'
        result, masked_result = self.service.check_guess(guess=guess, solution=solution)
        self.assertEqual(result, True)
        self.assertEqual(masked_result, '_oo')

    def test_check_wrong_guess(self):
        solution = 'foo'
        guess = 'z'
        result, masked_result = self.service.check_guess(guess=guess, solution=solution)
        self.assertEqual(result, False)
        self.assertEqual(masked_result, '___')


class TestCreateGame(TestHangmanService):

    @patch('src.infrastructure.services.hangman_service.HangmanGamesModel')
    def test_create_game(self, games_model_mock):
        self.service.get_masked_text = Mock()
        faker_instance = self.faker_mock.return_value
        solution = faker_instance.word.return_value
        user_id = self.faker.random_number()
        masked_word = self.service.get_masked_text.return_value
        game = games_model_mock.return_value

        created_game = self.service.create_game(user_id=user_id)
        self.assertEqual(created_game, game)
        expected_game_data = {
            'solution': solution,
            'attempts_left': 6,
            'status': GameStatus.IN_PROGRESS.value,
            'masked_word': masked_word,
            'user_id': user_id
        }
        games_model_mock.assert_called_once_with(**expected_game_data)
        self.db.session.add.assert_called_with(games_model_mock.return_value)
        self.db.session.commit.assert_called_once()


class TestGetGame(TestHangmanService):

    @patch('src.infrastructure.services.hangman_service.HangmanGamesModel')
    def test_get_game_return_game(self, games_model_mock):
        game_id = self.faker.random_number()
        user_id = self.faker.random_number()
        game_from_db = Mock()
        game_from_db.user_id = user_id
        games_model_mock.query.get_or_404.return_value = game_from_db

        game = self.service.get_game(game_id=game_id, user_id=user_id)
        self.assertEqual(game, game_from_db)

    @patch('src.infrastructure.services.hangman_service.HangmanGamesModel')
    def test_raise_exception_if_game_is_not_found(self, games_model_mock):
        games_model_mock.query.get_or_404.return_value = {}

        with self.assertRaises(GameNotFound):
            self.service.get_game('foo', 'baz')

    @patch('src.infrastructure.services.hangman_service.HangmanGamesModel')
    def test_raise_exception_if_user_id_mismatch(self, games_model_mock):
        games_model_mock.query.get_or_404.return_value.user_id = self.faker.random_number()

        with self.assertRaises(GameNotFound):
            self.service.get_game('foo', self.faker.random_number())


class TestFinishGame(TestHangmanService):
    def test_finish_game(self):
        attempts_left = self.faker.random_number()
        score = self.faker.random_number()
        game = Mock()
        game.attempts_left = attempts_left

        status = GameStatus.WON
        self.service.get_or_create_score = Mock()
        score_result = self.service.get_or_create_score.return_value
        score_result.score = score

        game_result = self.service.finish_game(game=game, status=status)
        self.assertEqual(game_result.status, status.value)
        self.assertEqual(score_result.score, score + attempts_left * 9)
        self.db.session.add_all.assert_called_once_with([game, score_result])
        self.db.session.commit.assert_called_once()


class TestSaveGame(TestHangmanService):
    def test_save_game(self):
        game = Mock()
        result = self.service.save_game(game=game)
        self.assertEqual(game, result)
        self.db.session.add.asser_called_once_with(game)
        self.db.session.commit.assert_called_once()


class TestGetAllGames(TestHangmanService):

    @patch('src.infrastructure.services.hangman_service.HangmanGamesModel')
    def test_get_all_games(self, games_model_mock):
        user_id = self.faker.random_number()
        result = self.service.get_all_games(user_id=user_id)
        self.assertEqual(result, games_model_mock.query.filter.return_value)


class TestHandleCorrectGuess(TestHangmanService):

    def test_finish_game_if_result_matches_solution(self):
        game = Mock()
        game.solution = 'foo'
        game.masked_word = 'f__'
        masked_result = '_oo'
        self.service.finish_game = Mock()

        result = self.service.handle_correct_guess(game=game, masked_result=masked_result)
        self.assertEqual(result, self.service.finish_game.return_value)
        self.service.finish_game.assert_called_once_with(game=game, status=GameStatus.WON)

    def test_save_game_if_result_matches_solution(self):
        game = Mock()
        game.solution = 'foo'
        game.masked_word = 'f__'
        masked_result = '__o'
        self.service.save_game = Mock()

        result = self.service.handle_correct_guess(game=game, masked_result=masked_result)
        self.assertEqual(result, self.service.save_game.return_value)


class TestHandleWrongGuess(TestHangmanService):

    def test_finish_game_if_attempts_reach_zero(self):
        game = Mock()
        game.attempts_left = 1
        self.service.finish_game = Mock()
        result = self.service.handle_wrong_guess(game=game)
        self.assertEqual(result, self.service.finish_game.return_value)
        self.service.finish_game.assert_called_once_with(game=game, status=GameStatus.LOST)

    def test_save_game_if_there_are_still_attempts_left(self):
        game = Mock()
        game.attempts_left = 2
        self.service.save_game = Mock()
        result = self.service.handle_wrong_guess(game=game)
        self.assertEqual(result, self.service.save_game.return_value)
        self.service.save_game.assert_called_once_with(game=game)


class TestTakeGuess(TestHangmanService):

    def test_correct_guess(self):
        game = Mock()
        game.status = GameStatus.IN_PROGRESS
        guess = self.faker.word()
        self.service.check_guess = Mock()
        self.service.check_guess.return_value = True, 'foo'

        self.service.handle_correct_guess = Mock()

        result = self.service.take_guess(guess=guess, game=game)
        self.assertEqual(result, self.service.handle_correct_guess.return_value)
        self.service.handle_correct_guess.assert_called_once_with(game=game, masked_result='foo')

    def test_wrong_guess(self):
        game = Mock()
        game.status = GameStatus.IN_PROGRESS
        guess = self.faker.word()
        self.service.check_guess = Mock()
        self.service.check_guess.return_value = False, 'foo'

        self.service.handle_wrong_guess = Mock()

        result = self.service.take_guess(guess=guess, game=game)
        self.assertEqual(result, self.service.handle_wrong_guess.return_value)
        self.service.handle_wrong_guess.assert_called_once_with(game=game)

    def test_raise_if_game_is_over(self):
        game = Mock()
        game.status = GameStatus.WON.value

        with self.assertRaises(GameOver):
            self.service.take_guess('f', game=game)

        game.status = GameStatus.LOST.value
        with self.assertRaises(GameOver):
            self.service.take_guess('f', game=game)


class TestGetOrCreateScore(TestHangmanService):

    @patch('src.infrastructure.services.hangman_service.HangmanScoresModel')
    def test_return_score_if_exists(self, score_model_mock):
        user_id = self.faker.random_number()

        res = self.service.get_or_create_score(user_id=user_id)
        self.assertEqual(res, score_model_mock.query.filter().first.return_value)

    @patch('src.infrastructure.services.hangman_service.HangmanScoresModel')
    def test_create_score_if_doesnt_exists(self, score_model_mock):
        user_id = self.faker.random_number()
        score_model_mock.query.filter().first.return_value = None
        expected_res = score_model_mock.return_value
        expected_res.user_id = user_id
        expected_res.score = 0

        res = self.service.get_or_create_score(user_id=user_id)
        self.assertEqual(res, expected_res)


class TestGetLeaderboard(TestHangmanService):

    @patch('src.infrastructure.services.hangman_service.HangmanScoresModel')
    def test_return_results(self, score_model_mock):
        mock_score = Mock()
        mock_score.user.name = self.faker.name()
        mock_score.score = self.faker.random_number()
        db_results = [
            mock_score
        ]
        self.db.session.query().all.return_value = db_results
        res = self.service.get_leaderboard()
        self.assertEqual(res, [{"name": mock_score.user.name, "score": mock_score.score}])
