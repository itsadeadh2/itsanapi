from rest_framework import viewsets, permissions

from api.models import Project
from api.serializers import (
    ProjectSerializer,
)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get_queryset(self):
        language = self.request.query_params.get("language", "")
        return Project.objects.filter(language__icontains=language)
