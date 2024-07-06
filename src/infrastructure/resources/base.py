from flask import jsonify
from flask.views import MethodView
from flask_smorest import abort
from logging import Logger
from abc import ABC

from src.infrastructure.exc import get_error_info


class BaseResource(ABC, MethodView):
    def __init__(self, logger: Logger):
        self.logger = logger

    def handle_error(self, status_code: int, exception: Exception):
        _, _, traceback = get_error_info()
        self.logger.error(str(exception))
        self.logger.error(traceback)
        return abort(status_code, exception)

    def send_response(self, status_code: int, *args, **kwargs):
        return jsonify(*args, **kwargs), status_code
