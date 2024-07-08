from src.database.db import db


class ExpiredTokensModel(db.Model):
    _tablename__ = "expired_tokens"

    jti = db.Column(db.String, primary_key=True)
