import unittest
from unittest.mock import Mock

from src.database.daos import EmailDAO
from src.infrastructure.exc import PersistenceError, DbLookupError


class TestEmailDAO(unittest.TestCase):
    def setUp(self):
        self.sqs = Mock()
        self.table = Mock()
        self.sqs.Table.return_value = self.table
        self.email_dao = EmailDAO(table_name='', db=self.sqs)

    def test_save_failure(self):
        self.table.put_item.side_effect = PersistenceError
        with self.assertRaises(PersistenceError):
            self.email_dao.save('foo@baz.com')

    def test_call_save_with_proper_params(self):
        email = 'foo@baz.com'
        self.email_dao.save(email)
        expected_call = {
            'Item': {
                'email': email
            }
        }
        self.table.put_item.assert_called_once_with(**expected_call)

    def test_query(self):
        response = self.email_dao.query()
        scan_mock = self.table.scan.return_value

        self.assertEqual(response, scan_mock.get.return_value)

    def test_query_failure(self):
        self.table.scan.side_effect = Exception('foo')
        with self.assertRaises(DbLookupError):
            self.email_dao.query()
