from flask import redirect, url_for, make_response, current_app
from flask_smorest import Blueprint
from injector import inject
from logging import Logger
from .base import BaseResource
from src.domain.handlers import AuthHandler

bp = Blueprint('auth', 'auth', description='Authentication routes')


@bp.route('/login')
class Login(BaseResource):
    @inject
    def __init__(self, logger: Logger, handler: AuthHandler):
        super().__init__(logger)
        self.handler = handler

    def get(self):
        try:
            return self.handler.handle_login_request()
        except Exception as e:
            self.handle_error(500, e)


@bp.route('/login/authorize')
class Authorize(BaseResource):

    @inject
    def __init__(self, logger: Logger, handler: AuthHandler):
        super().__init__(logger)
        self.handler = handler

    def get(self):
        token_info, user = self.handler.handle_authorization_callback()
        callback_url = current_app.config.get('FRONTEND_CALLBACK_URL')

        self.logger.info(user)
        flask_response = make_response(
            redirect(f'{callback_url}?access_token={token_info["access_token"]}&expires_at={token_info["expires_at"]}'))

        return flask_response


@bp.route('/logout')
class Logout(BaseResource):
    @inject
    def __init__(self, logger: Logger, handler: AuthHandler):
        super().__init__(logger)
        self.handler = handler

    def get(self):
        self.handler.handle_logout_request()
        return redirect(url_for('root.Root'))
