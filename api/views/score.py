from rest_framework import viewsets, permissions

from api.models import Score
from api.serializers import (
    ScoreSerializer,
)


class ScoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    lookup_field = "game__slug"

    def get_queryset(self):
        slug = self.request.query_params.get("filter", "")
        return Score.objects.filter(game__slug__icontains=slug)
