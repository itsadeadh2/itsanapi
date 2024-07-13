from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import ContactRequest, GameType, HangmanGame, Project, Score


class ContactRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = ['id', 'email', 'created']


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']


class GameSerializer(serializers.HyperlinkedModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = GameType
        fields = ['id', 'name', 'slug']
        lookup_field = 'slug'


class HangmanGameSerializer(serializers.HyperlinkedModelSerializer):
    solution = serializers.SerializerMethodField()
    attempts_left = serializers.ReadOnlyField()
    status = serializers.ReadOnlyField()
    masked_word = serializers.ReadOnlyField()
    player = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)

    class Meta:
        model = HangmanGame
        fields = [
            'id',
            'solution',
            'attempts_left',
            'status',
            'masked_word',
            'player'
        ]

    def get_solution(self, obj):
        if obj.status != HangmanGame.Status.IN_PROGRESS:
            return obj.solution
        return None


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        fields = [
            'name',
            'description',
            'language',
            'stack',
            'github_link',
            'docs_link'
        ]
        model = Project


class GuessSerializer(serializers.Serializer):
    guess = serializers.CharField(max_length=1)


class ScoreSerializer(serializers.ModelSerializer):
    player = serializers.ReadOnlyField(source='player.username')
    game = serializers.ReadOnlyField(source='game.name')

    class Meta:
        fields = [
            'score',
            'player',
            'game'
        ]
        model = Score
