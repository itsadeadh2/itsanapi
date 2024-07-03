from functools import wraps

from flask_oauthlib.client import OAuth
from flask import current_app, session, url_for, jsonify
from datetime import datetime
from datetime import UTC


oauth = OAuth()

google = oauth.remote_app(
    'google',
    app_key='GOOGLE',
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


def is_token_expired():
    token_info = session.get('google_token')
    if not token_info:
        return True
    expires_at = token_info.get('expires_at')
    if not expires_at:
        return True
    current_time = int(datetime.now(UTC).timestamp())
    return current_time > expires_at


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        login_url = url_for('auth.login')
        unauthorized_response = jsonify(message=f"The resource you're trying to access requires authentication. Go to {login_url}"), 401

        if is_token_expired():
            return unauthorized_response

        return f(*args, **kwargs)
    return decorated_function


def get_google():
    oauth.init_app(current_app)
    return google
