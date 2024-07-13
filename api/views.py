from django.contrib.auth.models import User
from django.utils.text import slugify
from faker import Faker
from rest_framework import status, permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import ContactRequest, GameType, HangmanGame, Project, Score
from api.serializers import (
    ContactRequestSerializer,
    UserSerializer,
    GameSerializer,
    HangmanGameSerializer,
    GuessSerializer,
    ProjectSerializer,
    ScoreSerializer,
)


class ContactRequestViewSet(viewsets.ModelViewSet):
    queryset = ContactRequest.objects.all()
    serializer_class = ContactRequestSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = GameType.objects.all()
    serializer_class = GameSerializer
    lookup_field = "slug"

    def perform_create(self, serializer):
        serializer.save(slug=slugify(serializer.validated_data["name"]))

    def perform_update(self, serializer):
        if "name" in serializer.validated_data:
            serializer.save(slug=slugify(serializer.validated_data["name"]))
        else:
            serializer.save()


class HangmanViewSet(viewsets.ModelViewSet):
    queryset = HangmanGame.objects.all()
    serializer_class = HangmanGameSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        try:
            game_type = GameType.objects.get(name="hangman")
            solution = Faker().word()
            game_data = {
                "solution": solution,
                "status": HangmanGame.Status.IN_PROGRESS,
                "masked_word": HangmanGame.get_masked_text(solution),
                "game": game_type,
                "player": self.request.user,
            }
            hangman = HangmanGame(**game_data)
            hangman.save()
            serializer = self.get_serializer(hangman)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except GameType.DoesNotExist:
            error_data = {"message": "No entry for hangman as gametype."}
            return Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=["POST"], url_path="guess")
    def guess(self, request, pk=None):
        guess = GuessSerializer(data=request.data)
        if not guess.is_valid():
            return Response(guess.errors)
        guess_letter = guess.validated_data.get("guess")

        game = self.get_object()
        if game.player.id != request.user.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        print(game.solution)
        if game.status != HangmanGame.Status.IN_PROGRESS:
            serializer = self.get_serializer(game)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if guess_letter in game.masked_word:
            return Response(
                {"message": "you already guessed this letter."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        game.handle_guess(letter=guess_letter)
        game.save()
        if game.status == HangmanGame.Status.WON:
            score, created = Score.objects.get_or_create(
                game=game.game, player=game.player
            )
            score.score += 9 * game.attempts_left
            score.save()
        serializer = self.get_serializer(game)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=False, methods=["POST"], url_path="bulk")
    def bulk(self, request):
        projects = []
        for entry in request.data:
            serializer = self.get_serializer(data=entry)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            projects.append(Project(**serializer.validated_data))

        Project.objects.bulk_create(projects)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ScoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    lookup_field = "game__slug"
