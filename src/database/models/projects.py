from src.database.db import (
    db,
)


class ProjectsModel(db.Model):
    __tablename__ = "projects"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    name = db.Column(
        db.String(120),
        unique=True,
        nullable=True,
    )
    description = db.Column(
        db.String(255),
        unique=True,
        nullable=True,
    )
    language = db.Column(
        db.String(120),
        unique=True,
        nullable=True,
    )
    stack = db.Column(
        db.String(120),
        unique=True,
        nullable=True,
    )
    github_link = db.Column(
        db.String(120),
        unique=True,
        nullable=True,
    )
    docs_link = db.Column(
        db.String(120),
        unique=True,
        nullable=True,
    )
