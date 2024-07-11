from logging import (
    Logger,
)

from flask_smorest import (
    Blueprint,
)
from injector import (
    inject,
)

from flask_jwt_extended import (
    get_jwt,
    jwt_required,
)
from src.infrastructure.schemas import (
    ProjectSchema,
)
from .base import (
    BaseResource,
)
from ...domain.handlers.projects_handler import (
    ProjectsHandler,
)

bp = Blueprint(
    "projects",
    "projects",
    description="Projects operations",
    url_prefix="/api",
)


@bp.route("/projects")
class Project(BaseResource):
    @inject
    def __init__(
        self,
        logger: Logger,
        projects_handler: ProjectsHandler,
    ):
        super().__init__(logger)
        self.handler = projects_handler

    @jwt_required()
    @bp.arguments(ProjectSchema)
    @bp.response(
        ProjectSchema,
        201,
    )
    def post(
        self,
        project_data,
    ):
        try:
            jwt = get_jwt()
            if not jwt.get("is_admin"):
                return self.send_response(
                    401,
                    message="Only admins can access this resource.",
                )
            return self.handler.create_project(project_data)
        except Exception as e:
            return self.handle_error(
                500,
                e,
            )

    @bp.response(
        ProjectSchema(many=True),
        200,
    )
    def get(
        self,
    ):
        try:
            return self.handler.get_projects()
        except Exception as e:
            return self.handle_error(
                500,
                e,
            )
