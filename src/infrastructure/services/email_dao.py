import boto3

from src.infrastructure.exc import PersistenceError, DbLookupError


class EmailDAO:
    def __init__(self, table_name, db=None):
        self.db = db or boto3.resource('dynamodb')
        self.table = self.db.Table(table_name)

    def save(self, email):
        try:
            self.table.put_item(
                Item={
                    'email': email,
                }
            )
        except Exception as e:
            raise PersistenceError(f"There was an error when saving the email {str(e)}")

    def query(self):
        try:
            response = self.table.scan()
            return response.get('Items', [])
        except Exception as e:
            raise DbLookupError(f"There was an error when querying the emails: {str(e)}")