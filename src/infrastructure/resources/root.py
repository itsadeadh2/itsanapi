from flask_smorest import Blueprint
from logging import Logger
from flask import redirect
from injector import inject
from.base import BaseResource

bp = Blueprint("root", "root", description="Root route operations")


@bp.route('/')
class Root(BaseResource):

    @inject
    def __init__(self, logger: Logger):
        super().__init__(logger)

    def get(self):
        return redirect('https://itsadeadh2.github.io/commodore-landing/', code=302)
