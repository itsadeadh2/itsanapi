from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework import permissions
from rest_framework.response import Response


@api_view(["GET"])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
def health_check(request):
    return Response(status=status.HTTP_200_OK)
