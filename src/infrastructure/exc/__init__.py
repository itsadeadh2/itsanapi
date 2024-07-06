import traceback
import sys


class InvalidEmailError(ValueError):
    pass


class PersistenceError(ValueError):
    pass


class DbLookupError(Exception):
    pass


class QueueInteractionError(ValueError):
    pass


class UserAlreadyExistsError(Exception):
    pass


class OAuthLoginFailure(Exception):
    pass


def get_error_info():
    (exception_type, exception_value, exception_traceback) = sys.exc_info()
    traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
    error_type = exception_type.__name__,
    error_message = str(exception_value),
    stack_trace = traceback_string,

    return error_type, error_message, stack_trace
