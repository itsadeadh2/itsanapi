from flask import Flask, redirect, url_for, session, request, jsonify, make_response
from flask_oauthlib.client import OAuth
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['OAUTH_CREDENTIALS'] = {
    'provider': {
        'id': 'your_client_id',
        'secret': 'your_client_secret'
    }
}

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

oauth = OAuth(app)
provider = oauth.remote_app(
    'provider',
    consumer_key=app.config['OAUTH_CREDENTIALS']['provider']['id'],
    consumer_secret=app.config['OAUTH_CREDENTIALS']['provider']['secret'],
    request_token_params={
        'scope': 'email',
    },
    base_url='https://api.provider.com/1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://api.provider.com/oauth/token',
    authorize_url='https://api.provider.com/oauth/authorize'
)

@provider.tokengetter
def get_provider_oauth_token():
    token = session.get('provider_token')
    if token:
        return token['access_token'], ''
    return None

@app.route('/login')
def login():
    return provider.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    response.delete_cookie('expires_at')
    return response

@app.route('/login/authorized')
def authorized():
    response = provider.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    expires_in = response.get('expires_in')
    expiration_time = datetime.utcnow() + timedelta(seconds=expires_in)
    expiration_unix = int(expiration_time.timestamp())

    # Create response and set cookies
    flask_response = make_response(redirect('http://localhost:3000/protected'))

    return flask_response
