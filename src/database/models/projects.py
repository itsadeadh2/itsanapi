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
        nullable=False,
        unique=False
    )
    description = db.Column(
        db.String(255),
        nullable=False,
        unique=False
    )
    language = db.Column(
        db.String(120),
        nullable=False,
        unique=False
    )
    stack = db.Column(
        db.String(255),
        nullable=False,
        unique=False
    )
    github_link = db.Column(
        db.String(120),
        nullable=False,
        unique=False
    )
    docs_link = db.Column(
        db.String(120),
        nullable=True,
        unique=False
    )
