from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from src.setup import add_cors, add_configs, add_resources, AppModule, add_db, add_jwt_config
from flask_injector import FlaskInjector


def create_app():
    app = Flask(__name__)

    add_configs(app)
    add_db(app)
    add_cors(app)
    add_resources(app)
    add_jwt_config(app)
    FlaskInjector(app=app, modules=[AppModule])

    return app


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    app = create_app()
    app.run(host='localhost', port=5000)
