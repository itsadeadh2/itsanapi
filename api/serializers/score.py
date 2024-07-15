from rest_framework import serializers

from api.models import Score


class ScoreSerializer(serializers.ModelSerializer):
    player = serializers.ReadOnlyField(source="player.first_name")
    game = serializers.ReadOnlyField(source="game.name")

    class Meta:
        fields = ["score", "player", "game"]
        model = Score
