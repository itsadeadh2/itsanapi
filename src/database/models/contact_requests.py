from sqlalchemy import func

from src.database.db import db


class ContactRequestsModel(db.Model):
    __tablename__ = 'contact_requests'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
