from injector import Module, provider, singleton
from src.infrastructure.services import Queue, EmailDAO
from src.domain.handlers import ContactHandler
from flask import current_app
from flask_oauthlib.client import OAuthRemoteApp
from src.infrastructure.services import get_google


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
    def provide_oauth(self) -> OAuthRemoteApp:
        return get_google()
