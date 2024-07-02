from flask_smorest import Blueprint
from flask.views import MethodView

bp = Blueprint("health", "health", description="Healthcheck operations")


@bp.route('/api/health')
class Health(MethodView):
    def get(self):
        return {'message': "I'm alive"}, 200

