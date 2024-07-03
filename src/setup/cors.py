from flask_cors import CORS


def add_cors(app):
    CORS(app, supports_credentials=True)
