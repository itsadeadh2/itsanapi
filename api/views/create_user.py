from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from api.serializers import (
    UserRegistrationSerializer,
)


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = UserRegistrationSerializer
