from src.infrastructure.services import Queue
from src.database.daos import EmailDAO


class ContactHandler:
    def __init__(
            self,
            email: EmailDAO,
            queue: Queue
    ):
        self.email = email
        self.queue = queue

    def handle_post(self, data):
        email = data.get('email', '')
        self.email.save(email)
        self.queue.add_to_queue(email)
        return {
            "message": f"Successfully received contact request. You should receive an email shortly on {email} with my contact information."}

    def handle_get(self):
        return self.email.query()
