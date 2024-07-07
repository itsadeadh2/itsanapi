from src.infrastructure.services import HangmanService, UserService


class HangmanHandler:
    def __init__(self, hangman_service: HangmanService, user_service: UserService):
        self.hangman_service = hangman_service
        self.user_service = user_service

    def create_game(self):
        user = self.user_service.get_user_from_token()
        return self.hangman_service.create_game(user_id=user.id)

    def get_game(self, game_id):
        user = self.user_service.get_user_from_token()
        return self.hangman_service.get_game(game_id=game_id, user_id=user.id)

    def take_guess(self, guess, game_id):
        game = self.get_game(game_id=game_id)
        return self.hangman_service.take_guess(
            guess=guess,
            game=game
        )

    def get_all_games(self):
        user = self.user_service.get_user_from_token()
        return self.hangman_service.get_all_games(user_id=user.id)

    def get_leaderboard(self):
        return self.hangman_service.get_leaderboard()
