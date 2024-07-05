from src.database.db import db
from flask_migrate import Migrate
from src.database.models import *


def add_db(app):
    db.init_app(app)
    return Migrate(app, db)
