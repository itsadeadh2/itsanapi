from flask_sqlalchemy import (
    SQLAlchemy,
)

from src.database.models import (
    ProjectsModel,
)


class ProjectsService:
    def __init__(
        self,
        db: SQLAlchemy,
    ):
        self.db = db

    def create_project(
        self,
        project_data,
    ):
        project = ProjectsModel(**project_data)
        self.db.session.add(project)
        self.db.session.commit()
        return project

    def get_projects(
        self,
    ):
        return ProjectsModel.query.all()
