from django.contrib.auth import authenticate, login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CustomLoginView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(self.request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response({'detail': 'CSRF cookie set'})
