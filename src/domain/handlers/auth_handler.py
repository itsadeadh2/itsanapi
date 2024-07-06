from injector import inject
from logging import Logger
from src.infrastructure.services import OAuthService, UserService


class AuthHandler:
    @inject
    def __init__(self, logger: Logger, oauth_service: OAuthService, user_service: UserService):
        self.logger = logger
        self.oauth_service = oauth_service
        self.user_service = user_service

    def handle_login_request(self):
        return self.oauth_service.send_authorization_request(flask_url='auth.Authorize')

    def handle_authorization_callback(self):
        token_info = self.oauth_service.retrieve_authorization_token()
        self.oauth_service.store_token_info_in_session(token_info=token_info)
        user_from_oauth = self.oauth_service.get_user_info()
        user_data = {
            'email': user_from_oauth['email'],
            'name': user_from_oauth['given_name'],
        }
        user_on_db = self.user_service.create_user(user_data=user_data)
        return token_info, user_on_db

    def handle_logout_request(self):
        self.oauth_service.log_user_out()
