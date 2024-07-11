from src.database.db import (
    db,
)


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=True,
    )
    name = db.Column(
        db.String(120),
        unique=False,
        nullable=False,
    )
    password = db.Column(
        db.String(255),
        nullable=False,
    )
    is_admin = db.Column(
        db.Boolean,
        default=False,
    )

    # Hangman games relationship
    hangman_games = db.relationship(
        "HangmanGamesModel",
        back_populates="user",
        lazy="dynamic",
        cascade="all, delete",
    )
    hangman_score = db.relationship(
        "HangmanScoresModel",
        back_populates="user",
        lazy="dynamic",
        cascade="all, delete",
    )
