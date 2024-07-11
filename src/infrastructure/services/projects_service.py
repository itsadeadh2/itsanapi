from flask_sqlalchemy import (
    SQLAlchemy,
)

from src.database.models import (
    ProjectsModel,
)


class ProjectsService:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create_project(self, project_data):
        project = ProjectsModel(**project_data)
        self.db.session.add(project)
        self.db.session.commit()
        return project

    def create_projects_in_bulk(self, projects):
        projects_list = [ProjectsModel(**project) for project in projects]
        self.db.session.add_all(projects_list)
        self.db.session.commit()
        return projects_list

    def get_projects(self, language=None):
        if not language:
            return ProjectsModel.query.all()
        return ProjectsModel.query.filter(ProjectsModel.language.ilike(f"%{language}%"))
