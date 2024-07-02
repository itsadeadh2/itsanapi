from flask_smorest import abort
from flask_smorest import Blueprint
from flask.views import MethodView
from src.infrastructure.services import Queue, EmailDAO
from src.domain.handlers import EmailHandler
from src.infrastructure.schemas import EmailSchema
from flask import current_app


bp = Blueprint("contact", "contact", description="Request contact info")


@bp.route('/api/contact')
class Contact(MethodView):
    def __init__(self, handler=None):
        self.handler = handler or EmailHandler(
            email=EmailDAO(
                table_name=current_app.config.get('TABLE_NAME')
            ),
            queue=Queue(
                queue_url=current_app.config.get('QUEUE_URL')
            )
        )

    @bp.arguments(EmailSchema)
    def post(self, email_data):
        try:
            data, status = self.handler.handle(email_data)
            return data, status
        except Exception as e:
            abort(500, e)
