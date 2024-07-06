from logging import Logger
from injector import inject
from src.infrastructure.services import OAuthService, UserService
from src.infrastructure.exc import GameCreationError
from src.database.daos import HangmanDao


class HangmanHandler:

    @inject
    def __init__(self, logger: Logger, oauth_service: OAuthService, user_service: UserService, hangman_dao: HangmanDao):
        self.__logger = logger
        self.__oauth = oauth_service
        self.__user = user_service
        self.__dao = hangman_dao

    def get_player_data(self):
        try:
            oauth_info = self.__oauth.get_user_info()
            return self.__user.get_user_by_email(oauth_info.get('email'))
        except Exception:
            return False

    def create_game(self):
        try:
            player_data = self.get_player_data()
            if not player_data:
                return self.create_guest_game()
            return self.create_user_game(player_data=player_data)
        except Exception as e:
            raise GameCreationError(str(e))

    def create_guest_game(self):
        return self.__dao.create_game()

    def create_user_game(self, player_data: dict):
        return self.__dao.create_game(player_data=player_data)
