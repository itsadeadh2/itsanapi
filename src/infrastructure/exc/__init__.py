class InvalidEmailError(ValueError):
    pass


class PersistenceError(ValueError):
    pass


class DbLookupError(Exception):
    pass


class QueueInteractionError(ValueError):
    pass
