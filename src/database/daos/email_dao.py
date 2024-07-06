from .base_dynamodb_dao import DynamoDAO
from src.infrastructure.exc import PersistenceError, DbLookupError


class EmailDAO (DynamoDAO):

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
