from abc import ABC


class DynamoDAO(ABC):
    def __init__(self, db, table_name):
        self.db = db
        self.table = self.db.Table(table_name)
