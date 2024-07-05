from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from src.setup import add_cors, add_configs, add_resources, AppModule, add_db
from flask_injector import FlaskInjector


def create_app():
    app = Flask(__name__)

    add_configs(app)
    migrate = add_db(app)
    add_cors(app)
    add_resources(app)
    FlaskInjector(app=app, modules=[AppModule])

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='localhost', port=5000)
