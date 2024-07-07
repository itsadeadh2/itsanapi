from logging import Logger

from flask import current_app
from flask_oauthlib.client import OAuth
from flask_oauthlib.client import OAuthRemoteApp
from flask_sqlalchemy import SQLAlchemy
from injector import Module, provider, singleton

from src.database.db import db
from src.domain.handlers import ContactHandler, UserHandler, HangmanHandler
from src.infrastructure.schemas import UserSchema
from src.infrastructure.services import (
    QueueService, ContactRequestService, UserService, HangmanService
)


# TODO: break this down into smaller components later
class AppModule(Module):
    @singleton
    @provider
    def provide_queue_service(self) -> QueueService:
        return QueueService(
            queue_url=current_app.config.get('QUEUE_URL')
        )

    @singleton
    @provider
    def provide_contact_request_service(self, database: SQLAlchemy) -> ContactRequestService:
        return ContactRequestService(db=database)

    @singleton
    @provider
    def provide_user_service(self, database: SQLAlchemy) -> UserService:
        return UserService(db=database)

    @singleton
    @provider
    def provide_hangman_service(self, database: SQLAlchemy) -> HangmanService:
        return HangmanService(db=database)

    @singleton
    @provider
    def provide_contact_handler(self, contact_request_service: ContactRequestService, queue: QueueService) -> ContactHandler:
        return ContactHandler(contact_request_service=contact_request_service, queue_service=queue)

    @singleton
    @provider
    def provide_user_handler(self, user_service: UserService) -> UserHandler:
        return UserHandler(user_service=user_service)

    @singleton
    @provider
    def provide_hangman_handler(self, hangman_service: HangmanService, user_service: UserService) -> HangmanHandler:
        return HangmanHandler(hangman_service=hangman_service, user_service=user_service)

    @singleton
    @provider
    def provide_logger(self) -> Logger:
        return current_app.logger

    @singleton
    @provider
    def provide_db(self) -> SQLAlchemy:
        return db

