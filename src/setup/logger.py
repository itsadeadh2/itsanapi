import logging
from logging import StreamHandler


def add_logger(app):
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Create a RotatingFileHandler to manage log file size
    handler = StreamHandler()

    # Create a formatter and set it for the handler
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)

    # Add the handler to the Flask app's logger
    app.logger.addHandler(handler)
