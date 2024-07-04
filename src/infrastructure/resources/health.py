from flask_smorest import Blueprint
from flask.views import MethodView
from logging import Logger
from injector import inject

bp = Blueprint("health", "health", description="Healthcheck operations")


@bp.route('/api/health')
class Health(MethodView):
    @inject
    def __init__(self, logger: Logger):
        self.logger = logger

    def get(self):
        self.logger.debug('debug')
        self.logger.info('info')
        self.logger.warning('warning')
        self.logger.error('error')
        self.logger.fatal('fatal')
        self.logger.critical('critical')
        return {'message': "I'm alive"}, 200
