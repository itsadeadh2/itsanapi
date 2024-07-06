from flask_smorest import Blueprint
from logging import Logger
from injector import inject
from .base import BaseResource
from src.infrastructure.flask_hooks.auth import add_user_to_request
from src.infrastructure.services import UserService, OAuthService

bp = Blueprint("health", "health", description="Healthcheck operations")


# Keeping this in here as a reference, this endpoint doesnt need it
#@bp.before_request
#@inject
#def before_request(logger: Logger, user_service: UserService, oauth_service: OAuthService):
#    res = add_user_to_request(user_service, oauth_service, logger)
#    if res:
#        return res

@bp.route('/api/health')
class Health(BaseResource):
    @inject
    def __init__(self, logger: Logger, user_service: UserService, oauth_service: OAuthService):
        super().__init__(logger)
        self.user_service = user_service
        self.oauth_service = oauth_service

    def get(self):
        return self.send_response(200, message="I'm alive")
