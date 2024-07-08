from src.infrastructure.services import ContactRequestService
from src.infrastructure.services import QueueService_


class ContactHandler:
    def __init__(
        self,
        contact_request_service: ContactRequestService,
        queue_service: QueueService_,
    ):
        self.contact_request_service = contact_request_service
        self.queue_service = queue_service

    def handle_post(self, data):
        email = data.get("email", "")
        self.contact_request_service.create_contact_request(email=email)
        self.queue_service.add_to_queue(email)
        return {
            "message": f"Successfully received contact request. You should receive an email shortly on {email} with my contact information."
        }

    def handle_get(self):
        return self.contact_request_service.get_all_contact_requests()
