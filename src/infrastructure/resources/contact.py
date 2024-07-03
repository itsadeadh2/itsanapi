from flask_smorest import abort
from flask_smorest import Blueprint
from flask.views import MethodView
from src.domain.handlers import ContactHandler
from src.infrastructure.schemas import EmailSchema
from injector import inject


bp = Blueprint("contact", "contact", description="Request contact info")


@bp.route('/api/contact')
class Contact(MethodView):
    @inject
    def __init__(self, handler: ContactHandler = None):
        self.handler = handler

    @bp.arguments(EmailSchema)
    def post(self, email_data):
        try:
            data, status = self.handler.handle_post(email_data)
            return data, status
        except Exception as e:
            abort(500, e)

    def get(self):
        try:
            data, status = self.handler.handle_get()
            return data, status
        except Exception as e:
            abort(500, e)
