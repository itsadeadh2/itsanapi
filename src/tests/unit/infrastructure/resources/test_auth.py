from .base_test import BaseResourcesTest


class BaseTestAuth(BaseResourcesTest):

    def setUp(self):
        super().setUp()

        self.auth_mock = self.mocks.get('auth_mock')
        self.logger_mock = self.mocks.get('logger_mock')


class TestAuthLogin(BaseTestAuth):

    def test_call_handler(self):
        fake_response = {}, 200
        self.auth_mock.handle_login_request.return_value = fake_response
        res = self.app.get('/login')
        self.auth_mock.handle_login_request.assert_called_once()
        self.assertEqual(res.status_code, 200)

    def test_return_500_if_exception_is_raised(self):
        self.auth_mock.handle_login_request.side_effect = Exception('foo')
        res = self.app.get('/login')
        self.auth_mock.handle_login_request.assert_called_once()
        self.assertEqual(res.status_code, 500)


class TestLoginAuthorize(BaseTestAuth):
    def test_call_handler(self):
        dummy_token_info = {
            'access_token': '',
            'expires_at': ''
        }
        dummy_user = {}
        self.auth_mock.handle_authorization_callback.return_value = dummy_token_info, dummy_user
        res = self.app.get('/login/authorize')
        self.auth_mock.handle_authorization_callback.assert_called_once()
        self.assertEqual(res.status_code, 302)


class TestLogout(BaseTestAuth):

    def test_call_handler(self):
        res = self.app.get('/logout')
        self.auth_mock.handle_logout_request.assert_called_once()
        self.assertEqual(res.status_code, 302)
