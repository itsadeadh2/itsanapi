from src.infrastructure.services import UserService


class UserHandler:

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def create_user(self, user_data):
        self.user_service.create_user(user_data)

    def log_in_user(self, user_data):
        return self.user_service.log_in_user(user_data=user_data)

    def log_out_user(self):
        return self.user_service.log_out_user()
