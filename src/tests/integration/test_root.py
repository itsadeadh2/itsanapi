from src.tests.integration.base_test import BaseTest


class TestRoot(BaseTest):

    def test_root(self):
        res = self.app.get("/")
        self.assertEqual(res.status_code, 302)
