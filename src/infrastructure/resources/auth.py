from flask import redirect, url_for, session, make_response, current_app
from flask_smorest import Blueprint
from datetime import datetime, timedelta
from datetime import UTC
from injector import inject
from flask_oauthlib.client import OAuthRemoteApp
from logging import Logger
from .base import BaseResource


bp = Blueprint('auth', 'auth', description='Authentication routes')


@bp.route('/login')
class Login(BaseResource):
    @inject
    def __init__(self, logger: Logger, oauth: OAuthRemoteApp = None):
        super().__init__(logger)
        self.oauth = oauth

    def get(self):
        try:
            return self.oauth.authorize(callback=url_for('auth.Authorize', _external=True))
        except Exception as e:
            self.handle_error(500, e)


@bp.route('/login/authorize')
class Authorize(BaseResource):

    @inject
    def __init__(self, logger: Logger, oauth: OAuthRemoteApp = None):
        super().__init__(logger)
        self.oauth = oauth

    def get(self):
        response = self.oauth.authorized_response()
        if response is None or response.get('access_token') is None:
            return self.send_response(401, message='Login failed.')

        expires_at = datetime.now(UTC) + timedelta(seconds=response.get('expires_in', 0))
        expires_at_unix = int(expires_at.timestamp())
        token_info = {**response, 'expires_at': expires_at_unix}

        session['google_token'] = token_info
        callback_url = current_app.config.get('FRONTEND_CALLBACK_URL')

        flask_response = make_response(
            redirect(f'{callback_url}?access_token={response["access_token"]}&expires_at={expires_at_unix}'))

        return flask_response


@bp.route('/logout')
class Logout(BaseResource):
    @inject
    def __init__(self, logger: Logger):
        super().__init__(logger)

    def get(self):
        session.pop('google_token', None)
        session.pop('refresh_token', None)
        return redirect(url_for('root.Root'))
