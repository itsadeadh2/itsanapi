import os
from flask import (
    jsonify,
)
from flask_jwt_extended import (
    JWTManager,
)

from src.database.models import (
    ExpiredTokensModel,
    UserModel,
)


def add_jwt_config(
    app,
):
    is_production = True if os.getenv("IS_PRODUCTION") else False

    app.config["JWT_SECRET_KEY"] = os.getenv(
        "foobarasidikas0901234-0apmasmca90==-=023)09)(*(&¨&560-0)¨*)((78987"
    )
    app.config["JWT_TOKEN_LOCATION"] = [
        "headers",
        "cookies",
    ]
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
    if is_production:
        app.config["JWT_SECRET_KEY"] = os.getenv(
            "JWT_SECRET_KEY",
            "foobarasidikas0901234-0apmasmca90==-=023)09)(*(&¨&560-0)¨*)((78987",
        )
        app.config["JWT_TOKEN_LOCATION"] = [
            "headers",
            "cookies",
        ]
        app.config["JWT_COOKIE_DOMAIN"] = ".itsadeadh2.com"
        app.config["JWT_COOKIE_SAMESITE"] = "None" if is_production else "Lax"
        app.config["JWT_COOKIE_SECURE"] = is_production
        app.config["JWT_ACCESS_COOKIE_PATH"] = "/"
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(
        identity,
    ):
        user = UserModel.query.get_or_404(identity)
        return {"is_admin": user.is_admin}

    @jwt.expired_token_loader
    def expired_token_callback(
        jwt_header,
        jwt_payload,
    ):
        return (
            jsonify(
                {
                    "message": "the token has expired.",
                    "error": "token_expired",
                }
            ),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(
        error,
    ):
        return jsonify(
            {
                "message": "Signature verification failed",
                "error": "invalid_token",
            },
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(
        error,
    ):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(
        jwt_header,
        jwt_payload,
    ):
        token = ExpiredTokensModel.query.get(jwt_payload["jti"])
        return bool(token)

    @jwt.revoked_token_loader
    def revoked_token_callback(
        jwt_header,
        jwt_payload,
    ):
        return (
            jsonify(
                {
                    "description": "The token has been revoked.",
                    "error": "token_revoked",
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(
        jwt_header,
        jwt_payload,
    ):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )
