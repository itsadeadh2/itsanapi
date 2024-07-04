from flask import jsonify
from flask.views import MethodView
from flask_smorest import abort
from logging import Logger
from abc import ABC


class BaseResource(ABC, MethodView):
    def __init__(self, logger: Logger):
        self.logger = logger

    def handle_error(self, status_code: int, exception: Exception):
        self.logger.error(str(exception))
        return abort(status_code, exception)

    def send_response(self, status_code: int, *args, **kwargs):
        return jsonify(*args, **kwargs), status_code
