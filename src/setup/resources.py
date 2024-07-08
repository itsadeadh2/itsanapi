from flask_smorest import Api

from src.infrastructure.resources import (
    health_bp,
    root_bp,
    contact_bp,
    user_bp,
    hangman_bp,
)


def add_resources(app):
    api = Api(app)

    api.register_blueprint(contact_bp)
    api.register_blueprint(health_bp)
    api.register_blueprint(root_bp)
    api.register_blueprint(user_bp)
    api.register_blueprint(hangman_bp)
