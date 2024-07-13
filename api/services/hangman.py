from faker import Faker

from api.models import GameType, HangmanGame, Score


class HangmanService:
    class GameTypeNotFound(Exception):
        pass

    class LetterAlreadyGuessed(Exception):
        pass

    @staticmethod
    def create_game_for_user(user) -> HangmanGame:
        try:
            game_type = GameType.objects.get(name="hangman")
            solution = Faker().word()
            game_data = {
                "solution": solution,
                "status": HangmanGame.Status.IN_PROGRESS,
                "masked_word": HangmanGame.get_masked_text(solution),
                "game": game_type,
                "player": user,
            }
            game = HangmanGame(**game_data)
            game.save()
            return game
        except GameType.DoesNotExist:
            raise HangmanService.GameTypeNotFound

    @staticmethod
    def take_guess(guess_letter: str, game: HangmanGame) -> HangmanGame:
        if game.status != HangmanGame.Status.IN_PROGRESS:
            return game

        if guess_letter in game.masked_word:
            raise HangmanService.LetterAlreadyGuessed

        game.handle_guess(letter=guess_letter)
        game.save()
        if game.status == HangmanGame.Status.WON:
            score, created = Score.objects.get_or_create(
                game=game.game, player=game.player
            )
            score.score += 9 * game.attempts_left
            score.save()
        return game
