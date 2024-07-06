from flask_smorest import Blueprint
from logging import Logger
from injector import inject
from src.infrastructure.resources.base import BaseResource
from src.domain.handlers import HangmanHandler

bp = Blueprint("hangman", "hangman", description="Resources for playing hangman game", url_prefix="/api/games")


@bp.route('/hangman')
class Start(BaseResource):
    @inject
    def __init__(self, logger: Logger, hangman_handler: HangmanHandler):
        super().__init__(logger)
        self.hangman = hangman_handler

    def post(self):
        try:
            created_game = self.hangman.create_game()
            return self.send_response(200, **created_game)
        except Exception as e:
            return self.handle_error(500, e)
