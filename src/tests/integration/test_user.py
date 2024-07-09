from src.tests.integration.base_test import BaseTest
from faker import Faker


class TestRegisterUser(BaseTest):

    user_data = {
        "name": Faker().name(),
        "email": Faker().email(),
        "password": Faker().password(),
    }

    def assert_status_code(self, data, status_code):
        res = self.app.post("/api/user/register", json=data)
        self.assertEqual(res.status_code, status_code)

    def test_register_successfully(self):
        self.assert_status_code(self.user_data, 201)

    def test_user_already_exists(self):
        self.assert_status_code(self.user_data, 201)
        self.assert_status_code(self.user_data, 409)

    def test_user_data_invalid(self):
        user_data = {}
        self.assert_status_code(user_data, 422)

        user_data = {"email": Faker().email()}
        self.assert_status_code(user_data, 422)

        user_data = {"email": Faker().email(), "password": Faker().password()}
        self.assert_status_code(user_data, 422)

        user_data = {"email": Faker().email(), "name": Faker().name()}
        self.assert_status_code(user_data, 422)

        user_data = {
            "email": "invalidmail.com",
            "name": Faker().name(),
            "password": Faker().password(),
        }
        self.assert_status_code(user_data, 422)


class TestLoginUser(BaseTest):
    def setUp(self):
        super().setUp()
        self.user_data = {
            "name": Faker().name(),
            "email": Faker().email(),
            "password": Faker().password(),
        }
        self.login = {
            "email": self.user_data.get("email"),
            "password": self.user_data.get("password"),
        }
        self.app.post("/api/user/register", json=self.user_data)

    def test_invalid_credentials(self):
        login = {"email": "nonexisting@user.com", "password": "123"}
        res = self.app.post("/api/user/login", json=login)
        self.assertEqual(res.status_code, 401)

        login = {"email": self.login.get("email"), "password": "123"}
        res = self.app.post("/api/user/login", json=login)
        self.assertEqual(res.status_code, 401)

    def test_return_access_token(self):
        res = self.app.post("/api/user/login", json=self.login)
        self.assertEqual(res.status_code, 200)
        has_access_token = "access_token" in res.get_json()
        self.assertEqual(True, has_access_token)


class TestLogoutUser(BaseTest):
    def setUp(self):
        super().setUp()
        user_data = {
            "name": Faker().name(),
            "email": Faker().email(),
            "password": Faker().password(),
        }
        login = {"email": user_data.get("email"), "password": user_data.get("password")}
        self.app.post("/api/user/register", json=user_data)
        res = self.app.post("/api/user/login", json=login)
        data = res.get_json()
        self.access_token = data.get("access_token")

    def test_error_if_not_logged_in(self):
        res = self.app.post("/api/user/logout")
        self.assertEqual(res.status_code, 401)

    def test_invalidate_token(self):
        res = self.app.post(
            "/api/user/logout", headers={"Authorization": f"Bearer {self.access_token}"}
        )
        self.assertEqual(res.status_code, 200)

        # second try should return 401 bc token was invalidated
        res = self.app.post(
            "/api/user/logout", headers={"Authorization": f"Bearer {self.access_token}"}
        )
        self.assertEqual(res.status_code, 401)
