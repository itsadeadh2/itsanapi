from src.tests.integration.base_test import BaseTest
from faker import Faker
from src.infrastructure.schemas import ProjectSchema


class BaseProjectsTest(BaseTest):

    def setUp(self):
        super().setUp()
        _, access_token = self.create_user(is_admin=True)
        self.access_token = access_token
        self.faker = Faker()

    def create_project(self, project_data, access_token=None):
        return self.app.post(
            "/api/projects",
            json=project_data,
            headers={"Authorization": f"Bearer {access_token or self.access_token}"}
        )

    def get_project_data(self):
        return {
            "name": self.faker.text(),
            "description": self.faker.text(),
            "language": self.faker.word(),
            "stack": self.faker.text(),
            "github_link": self.faker.url(),
            "docs_link": self.faker.url()
        }


class TestCreateProject(BaseProjectsTest):

    def test_return_new_project(self):
        project_data = self.get_project_data()
        response = self.create_project(project_data=project_data)
        response_data = response.get_json()
        return_data_valid = not ProjectSchema().validate(response_data)

        self.assertEqual(response.status_code, 201)
        self.assertTrue(return_data_valid)

    def test_create_bulk(self):
        project_data = [self.get_project_data() for _ in range(self.faker.random_int(min=1, max=5))]
        response = self.app.post(
            "/api/projects/bulk",
            json=project_data,
            headers={"Authorization": f"Bearer {self.access_token}"}
        )
        response_data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response_data), len(project_data))

    def test_create_bulk_return_401_if_not_admin(self):
        _, access_token = self.create_user(is_admin=False)
        project_data = [self.get_project_data() for _ in range(self.faker.random_int(min=1, max=5))]
        response = self.app.post(
            "/api/projects/bulk",
            json=project_data,
            headers={"Authorization": f"Bearer {access_token}"}
        )
        self.assertEqual(response.status_code, 401)

    def test_return_401_if_not_admin(self):
        _, access_token = self.create_user(is_admin=False)
        project_data = self.get_project_data()
        response = self.create_project(project_data=project_data, access_token=access_token)

        self.assertEqual(response.status_code, 401)


class TestGetProjects(BaseProjectsTest):

    def test_return_created_projects(self):
        fake_projects = [
            self.get_project_data() for _ in range(self.faker.random_int(min=1, max=5))
        ]

        for project in fake_projects:
            self.create_project(project)

        res = self.app.get("/api/projects")
        response_data = res.get_json()

        self.assertEqual(len(response_data), len(fake_projects))
        self.assertEqual(res.status_code, 200)

    def test_return_projects_by_language(self):

        # set up two lists of projects, each with one language
        language1 = self.faker.word()
        language2 = self.faker.word()

        l1_projects = [
            {**self.get_project_data(), 'language': language1} for _ in range(self.faker.random_int(min=1, max=5))
        ]
        l2_projects = [
            {**self.get_project_data(), 'language': language2} for _ in range(self.faker.random_int(min=1, max=5))
        ]

        # create the projects in both lists
        for project in [*l1_projects, *l2_projects]:
            self.create_project(project)

        # check language1
        l1_res = self.app.get(f"/api/projects?language={language1}")
        l1_data = l1_res.get_json()
        self.assertEqual(len(l1_data), len(l1_projects))
        self.assertEqual(l1_res.status_code, 200)
        for proj in l1_data:
            self.assertEqual(proj['language'], language1)

        # check language2
        l2_res = self.app.get(f"/api/projects?language={language2}")
        l2_data = l2_res.get_json()
        self.assertEqual(len(l2_data), len(l2_projects))
        self.assertEqual(l2_res.status_code, 200)
        for proj in l2_data:
            self.assertEqual(proj['language'], language2)
