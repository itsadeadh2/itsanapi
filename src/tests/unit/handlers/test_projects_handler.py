import unittest
from unittest.mock import Mock

from faker import Faker

from src.domain.handlers import ProjectsHandler


class TestProjectsHandler(unittest.TestCase):

    def setUp(self):
        self.faker = Faker()
        self.projects_service = Mock()
        self.handler = ProjectsHandler(
            projects_service=self.projects_service
        )

    def test_init_success(self):
        raised = False
        try:
            ProjectsHandler(
                projects_service=self.projects_service
            )
        except Exception:
            raised = True

        self.assertEqual(False, raised)

    def test_init_failure(self):
        with self.assertRaises(Exception):
            ProjectsHandler()

    def test_create_project(self):
        project_data = Mock()
        res = self.handler.create_project(project_data)
        self.projects_service.create_project.assert_called_once_with(project_data)
        self.assertEqual(res, self.projects_service.create_project.return_value)

    def test_create_in_bulk(self):
        projects_list = []
        res = self.handler.create_projects_in_bulk(projects_list)
        self.projects_service.create_projects_in_bulk.assert_called_once_with(projects_list)
        self.assertEqual(res, self.projects_service.create_projects_in_bulk.return_value)

    def test_get_projects(self):
        language = Mock()
        res = self.handler.get_projects(language=language)
        self.projects_service.get_projects.assert_called_once_with(language=language)
        self.assertEqual(res, self.projects_service.get_projects.return_value)
