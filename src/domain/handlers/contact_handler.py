from src.infrastructure.exc import InvalidEmailError, PersistenceError, QueueInteractionError, DbLookupError
from src.infrastructure.services import EmailDAO, Queue


class ContactHandler:
    def __init__(
            self,
            email: EmailDAO,
            queue: Queue
    ):
        self.email = email
        self.queue = queue

    def handle_post(self, data):
        try:
            email = data.get('email', '')
            self.email.save(email)
            self.queue.add_to_queue(email)
            return {
                "message": f"Successfully received contact request. You should receive an email shortly on {email} with my contact information."}, 200
        except InvalidEmailError as e:
            return {"message": str(e)}, 400
        except PersistenceError as e:
            return {"message": str(e)}, 500
        except QueueInteractionError as e:
            return {"message": str(e)}, 500

    def handle_get(self):
        try:
            emails = self.email.query()
            return {"emails": emails}, 200
        except DbLookupError as e:
            print(e)
            return {"mesage": str(e)}, 500
