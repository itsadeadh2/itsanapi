from src.infrastructure.services import (
    ProjectsService,
)


class ProjectsHandler:
    def __init__(
        self,
        projects_service: ProjectsService,
    ):
        self.service = projects_service

    def create_project(
        self,
        project_data,
    ):
        return self.service.create_project(project_data)

    def get_projects(
        self,
    ):
        return self.service.get_projects()
