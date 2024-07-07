class DynamoDB:
    def __init__(self, db, table_name):
        self.table = db.Table(table_name)
