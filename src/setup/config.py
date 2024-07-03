import os


def add_configs(app):
    # Configs from env vars #
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'TOP SECRET KEY!')
    app.config["TABLE_NAME"] = os.getenv("TABLE_NAME")
    app.config["QUEUE_URL"] = os.getenv("QUEUE_URL")
    app.config['GOOGLE'] = {
        'consumer_key': os.getenv('GOOGLE_CLIENT_ID'),
        'consumer_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
    }
    app.config["FRONTEND_CALLBACK_URL"] = os.getenv('FRONTEND_CALLBACK_URL')

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "ITSADEADH2 API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
