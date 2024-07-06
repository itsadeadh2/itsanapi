from flask_smorest import Blueprint
from src.domain.handlers import ContactHandler
from src.infrastructure.schemas import EmailSchema
from injector import inject
from logging import Logger
from .base import BaseResource
from src.infrastructure.exc import InvalidEmailError, PersistenceError, QueueInteractionError, DbLookupError

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
            data = self.handler.handle_post(email_data)
            return data, 200
        except InvalidEmailError as e:
            return self.handle_error(400, e)
        except PersistenceError as e:
            return self.handle_error(500, e)
        except QueueInteractionError as e:
            return self.handle_error(500, e)
        except Exception as e:
            return self.handle_error(500, e)

    def get(self):
        try:
            emails = self.handler.handle_get()
            data = {'emails': emails}
            return data, 200
        except DbLookupError as e:
            return self.handle_error(500, e)
        except Exception as e:
            return self.handle_error(500, e)
