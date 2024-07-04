from flask_smorest import Blueprint
from src.domain.handlers import ContactHandler
from src.infrastructure.schemas import EmailSchema
from injector import inject
from logging import Logger
from .base import BaseResource


bp = Blueprint("contact", "contact", description="Request contact info")


@bp.route('/api/contact')
class Contact(BaseResource):
    @inject
    def __init__(self, logger: Logger, handler: ContactHandler = None):
        super().__init__(logger)
        self.handler = handler

    @bp.arguments(EmailSchema)
    def post(self, email_data):
        try:
            data, status = self.handler.handle_post(email_data)
            return data, status
        except Exception as e:
            self.handle_error(500, e)

    def get(self):
        try:
            data, status = self.handler.handle_get()
            return data, status
        except Exception as e:
            self.handle_error(500, e)
