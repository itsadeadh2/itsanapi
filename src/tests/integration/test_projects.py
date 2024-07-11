from src.tests.integration.base_test import (
    BaseTest,
)
from faker import (
    Faker,
)
from src.infrastructure.schemas import (
    ProjectSchema,
)


class BaseProjectsTest(BaseTest):

    def setUp(
        self,
    ):
        super().setUp()
        (
            _,
            access_token,
        ) = self.create_user(is_admin=True)
        self.access_token = access_token
        self.faker = Faker()

    def create_project(
        self,
        project_data,
        access_token=None,
    ):
        return self.app.post(
            "/api/projects",
            json=project_data,
            headers={"Authorization": f"Bearer {access_token or self.access_token}"},
        )

    def get_project_data(
        self,
    ):
        return {
            "name": self.faker.text(),
            "description": self.faker.text(),
            "language": self.faker.word(),
            "stack": self.faker.text(),
            "github_link": self.faker.url(),
            "docs_link": self.faker.url(),
        }


class TestCreateProject(BaseProjectsTest):
    def test_return_new_project(
        self,
    ):
        project_data = self.get_project_data()
        response = self.create_project(project_data=project_data)
        response_data = response.get_json()
        return_data_valid = (
            True if not ProjectSchema().validate(response_data) else False
        )
        self.assertEqual(
            response.status_code,
            201,
        )
        self.assertEqual(
            True,
            return_data_valid,
        )

    def test_return_401_if_not_admin(
        self,
    ):
        (
            _,
            access_token,
        ) = self.create_user(is_admin=False)
        project_data = self.get_project_data()
        response = self.create_project(
            project_data=project_data,
            access_token=access_token,
        )
        self.assertEqual(
            response.status_code,
            401,
        )


class TestGetProjects(BaseProjectsTest):
    def test_return_created_projects(
        self,
    ):
        fake_projects = [
            self.get_project_data()
            for _ in range(
                self.faker.random_int(
                    max=5,
                    min=1,
                )
            )
        ]
        for project in fake_projects:
            self.create_project(project)

        res = self.app.get("/api/projects")
        response_data = res.get_json()
        self.assertEqual(
            len(response_data),
            len(fake_projects),
        )
        self.assertEqual(
            res.status_code,
            200,
        )
