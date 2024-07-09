from src.infrastructure.services import UserService, HangmanService


class UserHandler:

    def __init__(self, user_service: UserService, hangman_service: HangmanService):
        self.user_service = user_service
        self.hangman_service = hangman_service

    def create_user(self, user_data):
        user, access_token = self.user_service.create_user(user_data)
        self.hangman_service.get_or_create_score(user_id=user.id)
        return access_token

    def log_in_user(self, user_data):
        return self.user_service.log_in_user(user_data=user_data)

    def log_out_user(self):
        return self.user_service.log_out_user()
