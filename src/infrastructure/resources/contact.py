from flask_smorest import abort
from flask_smorest import Blueprint
from flask.views import MethodView
from src.infrastructure.services import Queue, EmailDAO
from src.domain.handlers import ContactHandler
from src.infrastructure.schemas import EmailSchema
from flask import current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify


bp = Blueprint("contact", "contact", description="Request contact info")


@bp.route('/api/contact')
class Contact(MethodView):
    def __init__(self, handler=None):
        self.handler = handler or ContactHandler(
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
            data, status = self.handler.handle_post(email_data)
            return data, status
        except Exception as e:
            abort(500, e)

    @jwt_required()
    def get(self):
        try:
            data, status = self.handler.handle_get()
            return data, status
        except Exception as e:
            abort(500, e)
