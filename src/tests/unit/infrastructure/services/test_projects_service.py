import unittest
from unittest.mock import Mock, patch

from faker import Faker

from src.infrastructure.services import ProjectsService


class TestProjectsService(unittest.TestCase):

    def setUp(self):
        self.db = Mock()
        self.faker = Faker()
        self.service = ProjectsService(db=self.db)

    def test_init_success(self):
        raised = False
        try:
            ProjectsService(db=self.db)
        except Exception:
            raised = True

        self.assertEqual(False, raised)

    def test_init_failure(self):
        with self.assertRaises(Exception):
            ProjectsService()


class TestCreateProject(TestProjectsService):

    @patch("src.infrastructure.services.projects_service.ProjectsModel")
    def test_creates_project_with_project_data(self, projects_model_mock):
        project_data = {"name": self.faker.text(), "description": self.faker.text()}
        res = self.service.create_project(project_data)
        projects_model_mock.assert_called_once_with(**project_data)
        self.db.session.add.assert_called_once_with(projects_model_mock.return_value)
        self.db.session.commit.assert_called_once()
        self.assertEqual(res, projects_model_mock.return_value)


class TestCreateProjectInBulk(TestProjectsService):

    @patch("src.infrastructure.services.projects_service.ProjectsModel")
    def test_creates_project_with_project_data(self, projects_model_mock):
        project_data = {"name": self.faker.text(), "description": self.faker.text()}
        project_list = [project_data for _ in range(self.faker.random_int(min=1, max=10))]

        self.service.create_projects_in_bulk(project_list)

        self.assertEqual(projects_model_mock.call_count, len(project_list))
        self.db.session.add_all.assert_called_once()
        self.db.session.commit.assert_called_once()


class TestGetProjects(TestProjectsService):

    @patch("src.infrastructure.services.projects_service.ProjectsModel")
    def test_return_all_if_no_language(self, projects_model_mock):
        res = self.service.get_projects()
        projects_model_mock.query.all.assert_called_once()
        self.assertEqual(res, projects_model_mock.query.all.return_value)

    @patch("src.infrastructure.services.projects_service.ProjectsModel")
    def test_return_filtered_results_if_language_is_given(self, projects_model_mock):
        language = self.faker.word()
        res = self.service.get_projects(language=language)

        projects_model_mock.query.filter.assert_called_once()
        self.assertEqual(res, projects_model_mock.query.filter.return_value)
