from flask_smorest import Blueprint
from logging import Logger
from injector import inject
from .base import BaseResource

bp = Blueprint("health", "health", description="Healthcheck operations")


@bp.route('/api/health')
class Health(BaseResource):
    @inject
    def __init__(self, logger: Logger):
        super().__init__(logger)

    def get(self):
        self.logger.debug('debug')
        self.logger.info('info')
        self.logger.warning('warning')
        self.logger.error('error')
        self.logger.fatal('fatal')
        self.logger.critical('critical')
        return self.send_response(200, message="I'm alive")
