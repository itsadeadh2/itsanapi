from logging import Logger

from flask_oauthlib.client import OAuthRemoteApp
from flask import session, url_for
from datetime import datetime, timedelta
from datetime import UTC
from injector import inject
from src.infrastructure.exc import OAuthLoginFailure


class OAuthService:

    @inject
    def __init__(self, google: OAuthRemoteApp, logger: Logger):
        self.google = google
        self.logger = logger
        self._set_tokengetter()

    def _set_tokengetter(self):
        @self.google.tokengetter
        def get_google_oauth_token():
            return session.get('google_token')
        # Assign the decorated function to an instance attribute if needed
        self.get_google_oauth_token = get_google_oauth_token

    def send_authorization_request(self, flask_url: str):
        return self.google.authorize(callback=url_for(flask_url, _external=True))

    def retrieve_authorization_token(self):
        response = self.google.authorized_response()
        if response is None or response.get('access_token') is None:
            raise OAuthLoginFailure('Login failed.')

        expires_at = datetime.now(UTC) + timedelta(seconds=response.get('expires_in', 0))
        expires_at_unix = int(expires_at.timestamp())
        token_info = {**response, 'expires_at': expires_at_unix}
        return token_info

    def store_token_info_in_session(self, token_info):
        session['google_token'] = token_info

    def log_user_out(self):
        session.pop('google_token', None)
        session.pop('refresh_token', None)

    def get_user_info(self):
        response = self.get('userinfo')
        return response.data

    def get(self, endpoint: str):
        return self.google.get(endpoint)
