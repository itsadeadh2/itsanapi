from rest_framework import permissions
from rest_framework.generics import ListAPIView

from api.filters import ScoreFilters
from api.models import Score
from api.serializers import (
    ScoreSerializer,
)


class ScoreListView(ListAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    filterset_class = ScoreFilters
