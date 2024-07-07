from flask_sqlalchemy import SQLAlchemy

from src.database.models import ContactRequestsModel


class ContactRequestService:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create_contact_request(self, email):
        contact_request = ContactRequestsModel(email=email)
        self.db.session.add(contact_request)
        self.db.session.commit()
        return contact_request

    def get_all_contact_requests(self):
        return ContactRequestsModel.query.all()
