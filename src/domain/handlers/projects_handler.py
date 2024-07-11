from src.infrastructure.services import (
    ProjectsService,
)


class ProjectsHandler:
    def __init__(self, projects_service: ProjectsService):
        self.service = projects_service

    def create_project(self, project_data):
        return self.service.create_project(project_data)

    def create_projects_in_bulk(self, projects):
        return self.service.create_projects_in_bulk(projects)

    def get_projects(self, language=None):
        return self.service.get_projects(language=language)
