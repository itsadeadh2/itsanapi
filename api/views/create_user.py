from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from api.serializers import (
    UserRegistrationSerializer,
)


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = UserRegistrationSerializer
