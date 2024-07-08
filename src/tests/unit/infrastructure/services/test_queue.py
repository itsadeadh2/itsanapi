import unittest
from unittest.mock import Mock

from src.infrastructure.services import QueueService_


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.sqs = Mock()
        self.queue = QueueService_(queue_url="", sqs=self.sqs)

    def test_call_add_to_queue_with_proper_params(self):
        email = "foo@baz.com"
        self.queue.add_to_queue(email)
        expected_call = {"QueueUrl": "", "MessageBody": email}
        self.sqs.send_message.assert_called_once_with(**expected_call)
