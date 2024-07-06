import unittest
from unittest.mock import Mock
from src.domain.handlers import HangmanHandler
from faker import Faker


class TestBaseHangmanHandler(unittest.TestCase):
    def setUp(self):
        self.handler = HangmanHandler()
        self.fake = Faker()


class TestHangmanCreateGame(TestBaseHangmanHandler):

    def test_create_guest_game_if_no_user(self):
        pass
    def test_success(self):
        event = {'email': self.fake.email()}
        self.handler.handle_post(data=event)
        self.email.save.assert_called_once_with(event['email'])
        self.queue.add_to_queue.assert_called_once_with(event['email'])
