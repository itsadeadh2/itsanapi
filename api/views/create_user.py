from django.contrib.auth import authenticate, login
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

    def perform_create(self, serializer):
        super().perform_create(serializer=serializer)
        user = serializer.validated_data
        email = user.get("email")
        password = user.get("password")
        authenticated_user = authenticate(self.request, email=email, password=password)
        if authenticated_user:
            login(self.request, authenticated_user)
