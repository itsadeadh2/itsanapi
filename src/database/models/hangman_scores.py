from src.database.db import db


class HangmanScoresModel(db.Model):
    __tablename__ = 'hangman_scores'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, default=0, nullable=False)

    # Player relationship
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("UserModel", back_populates="hangman_score")


