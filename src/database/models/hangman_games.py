from src.database.db import db


class HangmanGamesModel(db.Model):
    __tablename__ = 'hangman_games'

    id = db.Column(db.Integer, primary_key=True)
    solution = db.Column(db.String(120), nullable=False)
    attempts_left = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(120), nullable=False)
    masked_word = db.Column(db.String(120), nullable=False)

    # Player relationship
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel", back_populates="hangman_games")
