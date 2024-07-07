import traceback
import sys


class UserAlreadyExists(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class GameNotFound(Exception):
    pass

class GameOver(Exception):
    pass



def get_error_info():
    (exception_type, exception_value, exception_traceback) = sys.exc_info()
    traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
    error_type = exception_type.__name__,
    error_message = str(exception_value),
    stack_trace = traceback_string,

    return error_type, error_message, stack_trace
