from flask import request, session, jsonify, url_for
from datetime import datetime, UTC
from src.infrastructure.services import UserService, OAuthService


def is_token_expired():
    token_info = session.get('google_token')
    if not token_info:
        return True
    expires_at = token_info.get('expires_at')
    if not expires_at:
        return True
    current_time = int(datetime.now(UTC).timestamp())
    return current_time > expires_at


def login_required():
    login_url = url_for('auth.login')
    unauthorized_response = jsonify(
        message=f"The resource you're trying to access requires authentication. Go to {login_url}"), 401

    if is_token_expired():
        return unauthorized_response


def add_user_to_request(user_service: UserService, oauth_service: OAuthService, logger):
    try:
        user_from_oauth = oauth_service.get_user_info()
        user = user_service.get_user_by_email(user_from_oauth.get('email'))
        request.user = user
    except Exception as e:
        logger.error("Failed to populate user information.", exc_info=e)
        request.user = {}
