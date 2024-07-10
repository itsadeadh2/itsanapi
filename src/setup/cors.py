from flask_cors import CORS


def add_cors(app):
    is_production = True if os.getenv("IS_PRODUCTION") else False
    if is_production:
        CORS(app, supports_credentials=True, resources={
            r"/api/*": {
                "origins": "https://itsadeadh2.github.io",
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "X-CSRF-TOKEN"],
                "expose_headers": ["X-CSRF-TOKEN"]
            }
        })
    else:
        CORS(app, supports_credentials=True, resources={
            r"/api/*": {
                "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "X-CSRF-TOKEN"],
                "expose_headers": ["X-CSRF-TOKEN"]
            }
        })
