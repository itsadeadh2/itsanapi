from rest_framework import viewsets, permissions

from api.filters import ProjectFilters
from api.models import Project
from api.serializers import (
    ProjectSerializer,
)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    filterset_class = ProjectFilters
