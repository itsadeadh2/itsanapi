from rest_framework import permissions
from rest_framework.generics import ListAPIView

from api.models import Score
from api.serializers import (
    ScoreSerializer,
)


class ScoreListView(ListAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        slug = self.request.query_params.get("filter", "")
        return Score.objects.filter(game__slug__icontains=slug)
