from flask_migrate import Migrate

from src.database.db import db
from src.database.models import (
    UserModel,
    HangmanGamesModel,
    HangmanScoresModel,
    ExpiredTokensModel,
    ContactRequestsModel,
)


def add_db(app):
    db.init_app(app)
    return Migrate(app, db)


__all__ = [
    "UserModel",
    "HangmanGamesModel",
    "HangmanScoresModel",
    "ExpiredTokensModel",
    "ContactRequestsModel",
]
