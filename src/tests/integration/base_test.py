import os
from unittest import (
    TestCase,
)

from faker import (
    Faker,
)

from src.app import (
    create_app,
)
from src.database.db import (
    db,
)
from src.database.models import (
    UserModel,
)


class BaseTest(TestCase):
    TEST_DATABASE_URI = "sqlite:///test.db"

    def setUp(
            self,
    ):
        os.environ["DATABASE_URL"] = self.TEST_DATABASE_URI
        app = create_app()
        self.app = app.test_client()
        self.app_context = app.app_context()

        with self.app_context:
            # Create all tables and apply migrations
            db.create_all()

    def tearDown(
            self,
    ):
        with self.app_context:
            # Drop all tables
            db.drop_all()

    def create_user(
            self,
            is_admin=False,
    ):
        user_data = {
            "name": Faker().name(),
            "email": Faker().email(),
            "password": Faker().password(),
        }
        login = {
            "email": user_data.get("email"),
            "password": user_data.get("password"),
        }
        self.app.post(
            "/api/user/register",
            json=user_data,
        )
        if is_admin:
            with self.app_context:
                user = UserModel.query.filter(
                    UserModel.email == user_data.get("email")
                ).first()
                user.is_admin = True
                db.session.add(user)
                db.session.commit()
        res = self.app.post(
            "/api/user/login",
            json=login,
        )
        data = res.get_json()
        access_token = data.get("access_token")
        return (
            user_data,
            access_token,
        )
