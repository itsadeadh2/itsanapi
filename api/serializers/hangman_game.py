from rest_framework import serializers

from api.models import HangmanGame


class HangmanGameSerializer(serializers.HyperlinkedModelSerializer):
    solution = serializers.SerializerMethodField()
    attempts_left = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    masked_word = serializers.ReadOnlyField()
    player = serializers.ReadOnlyField(source="player.username")

    class Meta:
        model = HangmanGame
        fields = ["id", "solution", "attempts_left", "status", "masked_word", "player"]

    def get_solution(self, obj):
        if obj.status != HangmanGame.Status.IN_PROGRESS:
            return obj.solution
        return None
