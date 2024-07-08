from enum import Enum

from faker import Faker
from flask_sqlalchemy import SQLAlchemy

from src.database.models import HangmanGamesModel, HangmanScoresModel
from src.infrastructure.exc import GameNotFound, GameOver


class GameStatus(Enum):
    IN_PROGRESS = 'GAME_IN_PROGRESS'
    WON = 'GAME_WON'
    LOST = 'GAME_LOST'


class HangmanService:
    def __init__(self, db: SQLAlchemy):
        self.db = db
        self.faker = Faker()

    # UTILS #
    def get_masked_text(self, text):
        return ''.join(['_' for x in text])

    def check_guess(self, guess: str, solution: str):
        success = False
        mask_result = ''
        for idx, c in enumerate(solution):
            char_result = '_'
            if guess.lower() == c.lower():
                success = True
                char_result = guess
            mask_result += char_result
        return success, mask_result

    # GAME LOGIC #
    def create_game(self, user_id):
        solution = self.faker.word()
        game_data = {
            'solution': solution,
            'attempts_left': 6,
            'status': GameStatus.IN_PROGRESS.value,
            'masked_word': self.get_masked_text(solution),
            'user_id': user_id
        }
        game = HangmanGamesModel(**game_data)
        self.db.session.add(game)
        self.db.session.commit()
        return game

    def get_game(self, game_id, user_id):
        try:
            game = HangmanGamesModel.query.get_or_404(game_id)
            if game and game.user_id == user_id:
                return game
            raise GameNotFound("Unable to find game")
        except Exception:
            raise GameNotFound("Unable to find game")

    def finish_game(self, game: HangmanGamesModel, status: GameStatus):
        game.status = status.value

        game_score = game.attempts_left * 9
        user_score = self.get_or_create_score(user_id=game.user_id)
        user_score.score += game_score

        self.db.session.add_all([game, user_score])
        self.db.session.commit()
        return game

    def save_game(self, game: HangmanGamesModel):
        self.db.session.add(game)
        self.db.session.commit()
        return game

    def get_all_games(self, user_id):
        return HangmanGamesModel.query.filter(HangmanGamesModel.user_id == user_id)

    # GUESS LOGIC #
    def handle_correct_guess(self, game: HangmanGamesModel, masked_result):
        merged_masked_result = list(game.masked_word)
        for idx, c in enumerate(masked_result):
            if c.lower() != '_':
                merged_masked_result[idx] = c
        game.masked_word = ''.join(merged_masked_result)

        if game.masked_word == game.solution:
            return self.finish_game(game=game, status=GameStatus.WON)
        return self.save_game(game=game)

    def handle_wrong_guess(self, game: HangmanGamesModel):
        game.attempts_left -= 1
        if game.attempts_left < 1:
            return self.finish_game(game=game, status=GameStatus.LOST)
        return self.save_game(game=game)

    def take_guess(self, guess, game: HangmanGamesModel):
        if game.status in [GameStatus.WON.value, GameStatus.LOST.value]:
            raise GameOver("Sorry but this game is already over.")

        solution = game.solution
        print(f'SOLUTION: {solution}')

        success, masked_result = self.check_guess(guess=guess, solution=solution)

        if success:
            return self.handle_correct_guess(game=game, masked_result=masked_result)
        return self.handle_wrong_guess(game=game)

    # SORE LOGIC #
    def get_or_create_score(self, user_id):
        score = HangmanScoresModel.query.filter(HangmanScoresModel.user_id == user_id).first()
        if not score:
            score = HangmanScoresModel()
            score.user_id = user_id
            score.score = 0
        self.db.session.add(score)
        self.db.session.commit()
        return score

    def get_leaderboard(self):
        results = self.db.session.query(HangmanScoresModel).all()

        scores = [
            {
                "name": score.user.name,
                "score": score.score
            }
            for score in results
        ]
        return scores
