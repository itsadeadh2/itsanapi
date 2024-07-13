from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from api.services import QueueService

from api.models import ContactRequest
from api.serializers import (
    ContactRequestSerializer,
)


class CreateContactRequestView(CreateAPIView):
    model = ContactRequest
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = ContactRequestSerializer

    def perform_create(self, serializer):
        email = serializer.validated_data.get("email")
        queue = QueueService()
        queue.add_to_queue(email=email)
        super().perform_create(serializer)
