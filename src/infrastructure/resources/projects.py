from logging import Logger

from flask_jwt_extended import get_jwt, jwt_required
from flask_smorest import Blueprint
from injector import inject

from src.domain.handlers.projects_handler import ProjectsHandler
from src.infrastructure.schemas import ProjectSchema
from .base import BaseResource
from flask import request
bp = Blueprint(
    "projects",
    "projects",
    description="Projects operations",
    url_prefix="/api"
)


@bp.route("/projects")
class Project(BaseResource):

    @inject
    def __init__(self, logger: Logger, projects_handler: ProjectsHandler):
        super().__init__(logger)
        self.handler = projects_handler

    @jwt_required()
    @bp.arguments(ProjectSchema)
    @bp.response(201, ProjectSchema)
    def post(self, project_data):
        try:
            jwt = get_jwt()
            if not jwt.get("is_admin"):
                return self.send_response(401, message="Only admins can access this resource.")
            return self.handler.create_project(project_data)
        except Exception as e:
            return self.handle_error(500, e)

    @bp.response(200, ProjectSchema(many=True))
    def get(self):
        try:
            language = request.args.get('language', '')
            return self.handler.get_projects(language=language)
        except Exception as e:
            return self.handle_error(500, e)


@bp.route("/projects/bulk")
class ProjectBulk(BaseResource):

    @inject
    def __init__(self, logger: Logger, projects_handler: ProjectsHandler):
        super().__init__(logger)
        self.handler = projects_handler

    @jwt_required()
    @bp.arguments(ProjectSchema(many=True))
    @bp.response(201, ProjectSchema(many=True))
    def post(self, project_data):
        try:
            jwt = get_jwt()
            if not jwt.get("is_admin"):
                return self.send_response(401, message="Only admins can access this resource.")
            return self.handler.create_projects_in_bulk(project_data)
        except Exception as e:
            return self.handle_error(500, e)
