from logging import Logger

from injector import Module, provider, singleton
from src.infrastructure.services import Queue, EmailDAO
from src.domain.handlers import ContactHandler, AuthHandler
from flask import current_app
from flask_oauthlib.client import OAuthRemoteApp
from flask_sqlalchemy import SQLAlchemy
from src.database.db import db
from src.infrastructure.services import UserService
from flask_oauthlib.client import OAuth
from src.infrastructure.services import OAuthService
from src.infrastructure.schemas import UserSchema


# TODO: break this down into smaller components later
class AppModule(Module):
    @singleton
    @provider
    def provide_email_dao(self) -> EmailDAO:
        return EmailDAO(
            table_name=current_app.config.get('TABLE_NAME')
        )

    @singleton
    @provider
    def provide_queue(self) -> Queue:
        return Queue(
            queue_url=current_app.config.get('QUEUE_URL')
        )

    @singleton
    @provider
    def provide_contact_handler(self, email_dao: EmailDAO, queue: Queue) -> ContactHandler:
        return ContactHandler(email=email_dao, queue=queue)

    @singleton
    @provider
    def provide_auth_handler(self, logger: Logger, oauth_service: OAuthService, user_service: UserService) -> AuthHandler:
        return AuthHandler(logger=logger, oauth_service=oauth_service, user_service=user_service)

    @singleton
    @provider
    def provide_oauth_client(self) -> OAuth:
        return OAuth()

    @singleton
    @provider
    def provide_oauth_remote_app(self, oauth: OAuth) -> OAuthRemoteApp:
        google = oauth.remote_app(
            'google',
            app_key='GOOGLE',
            request_token_params={
                'scope': 'email profile',
            },
            base_url='https://www.googleapis.com/oauth2/v1/',
            request_token_url=None,
            access_token_method='POST',
            access_token_url='https://accounts.google.com/o/oauth2/token',
            authorize_url='https://accounts.google.com/o/oauth2/auth',
        )
        oauth.init_app(current_app)
        return google

    @singleton
    @provider
    def provide_oauth_service(self, google: OAuthRemoteApp, logger: Logger) -> OAuthService:
        return OAuthService(google=google, logger=logger)

    @singleton
    @provider
    def provide_logger(self) -> Logger:
        return current_app.logger

    @singleton
    @provider
    def provide_db(self) -> SQLAlchemy:
        return db

    @singleton
    @provider
    def provide_user_service(self, database: SQLAlchemy, logger: Logger, user_schema: UserSchema) -> UserService:
        return UserService(db=database, logger=logger, user_schema=user_schema)

    @singleton
    @provider
    def provide_user_schema(self) -> UserSchema:
        return UserSchema()

