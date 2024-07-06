from logging import Logger
from injector import inject


class HangmanHandler:

    @inject
    def __init__(self, logger: Logger):
        self.__logger = logger

    def create_game(self):
        pass
