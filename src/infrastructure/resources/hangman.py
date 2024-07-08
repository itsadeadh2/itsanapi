from logging import Logger

from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from injector import inject

from src.domain.handlers import HangmanHandler
from src.infrastructure.exc import GameNotFound, GameOver
from src.infrastructure.schemas import (
    HangmanGameSchema,
    HangmanGuesSchema,
    HangmanScoreSchema,
)
from .base import BaseResource

bp = Blueprint(
    "hangman", "hangman", description="Play a game of hangman", url_prefix="/api/games"
)


@bp.route("/hangman")
class HangmanList(BaseResource):
    @inject
    def __init__(self, logger: Logger, handler: HangmanHandler):
        super().__init__(logger)
        self.handler = handler

    @jwt_required()
    @bp.response(201, HangmanGameSchema)
    def post(self):
        try:
            return self.handler.create_game()
        except Exception as e:
            return self.handle_error(500, e)

    @jwt_required()
    @bp.response(201, HangmanGameSchema(many=True))
    def get(self):
        try:
            return self.handler.get_all_games()
        except Exception as e:
            return self.handle_error(500, e)


@bp.route("/hangman/<string:game_id>")
class GetGame(BaseResource):
    @inject
    def __init__(self, logger: Logger, handler: HangmanHandler):
        super().__init__(logger)
        self.handler = handler

    @jwt_required()
    @bp.response(200, HangmanGameSchema)
    def get(self, game_id):
        try:
            return self.handler.get_game(game_id=game_id)
        except GameNotFound as e:
            return self.handle_error(404, e)
        except Exception as e:
            return self.handle_error(500, e)


@bp.route("/hangman/<string:game_id>/guess")
class TakeGuess(BaseResource):
    @inject
    def __init__(self, logger: Logger, handler: HangmanHandler):
        super().__init__(logger)
        self.handler = handler

    @jwt_required()
    @bp.arguments(HangmanGuesSchema)
    @bp.response(200, HangmanGameSchema)
    def post(self, guess_data, game_id):
        try:
            return self.handler.take_guess(
                game_id=game_id, guess=guess_data.get("guess")
            )
        except GameOver as e:
            return self.handle_error(400, e)


@bp.route("/hangman/leaderboard")
class LeaderBoardList(BaseResource):
    @inject
    def __init__(self, logger: Logger, handler: HangmanHandler):
        super().__init__(logger)
        self.handler = handler

    @bp.response(200, HangmanScoreSchema(many=True))
    def get(self):
        try:
            return self.handler.get_leaderboard()
        except Exception as e:
            return self.handle_error(500, e)
