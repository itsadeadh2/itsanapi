import os
from flask_cors import CORS


def add_cors(app):
    is_production = True if os.getenv("IS_PRODUCTION") else False
    CORS(app, supports_credentials=True)
