from logging import Logger
from flask import make_response, jsonify

from flask_jwt_extended import jwt_required, set_access_cookies
from flask_smorest import Blueprint
from injector import inject

from src.domain.handlers import UserHandler
from src.infrastructure.exc import UserAlreadyExists, InvalidCredentials
from src.infrastructure.schemas import UserSchema, UserLoginSchema
from .base import BaseResource

bp = Blueprint("user", "user", description="User operations", url_prefix="/api/user")


@bp.route("/register")
class Register(BaseResource):

    @inject
    def __init__(self, logger: Logger, user_handler: UserHandler):
        super().__init__(logger=logger)
        self.handler = user_handler

    @bp.arguments(UserSchema)
    def post(self, user_data):
        try:
            access_token = self.handler.create_user(user_data=user_data)
            response = make_response(
                jsonify(message="User created successfully", access_token=access_token),
                201,
            )
            set_access_cookies(response, access_token)
            return response
        except UserAlreadyExists as error:
            return self.handle_error(409, error)


@bp.route("/login")
class Login(BaseResource):

    @inject
    def __init__(self, logger: Logger, user_handler: UserHandler):
        super().__init__(logger=logger)
        self.handler = user_handler

    @bp.arguments(UserLoginSchema)
    def post(self, user_data):
        try:
            access_token = self.handler.log_in_user(user_data)
            response = make_response(jsonify(access_token=access_token), 200)
            set_access_cookies(response, access_token)
            return response
        except InvalidCredentials as error:
            return self.handle_error(401, error)


@bp.route("/logout")
class Logout(BaseResource):
    @inject
    def __init__(self, logger: Logger, user_handler: UserHandler):
        super().__init__(logger=logger)
        self.handler = user_handler

    @jwt_required()
    def post(self):
        self.handler.log_out_user()
        return self.send_response(200, message="Successfully logged out")
