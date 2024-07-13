from rest_framework import status, permissions
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response

from api.models import HangmanGame
from api.serializers import (
    HangmanGameSerializer,
    GuessSerializer,
)
from api.services import HangmanService


class HangmanListView(CreateAPIView, ListAPIView):
    queryset = HangmanGame.objects.all()
    serializer_class = HangmanGameSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            game = HangmanService.create_game_for_user(self.request.user)
            serializer = self.get_serializer(game)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except HangmanService.GameTypeNotFound:
            error_data = {"message": "No entry for hangman as game type."}
            return Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            error_data = {
                "message": "There was an error when bootstrapping your game. Please try again later."
            }
            return Response(error_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        user = self.request.user
        return HangmanGame.objects.filter(player=user)


class HangmanDetailView(RetrieveAPIView):
    queryset = HangmanGame.objects.all()
    serializer_class = HangmanGameSerializer
    permission_classes = [permissions.IsAuthenticated]


class HangmanGuessView(CreateAPIView):
    queryset = HangmanGame.objects.all()
    serializer_class = HangmanGameSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            guess = GuessSerializer(data=request.data)
            if not guess.is_valid():
                return Response(guess.errors, status=status.HTTP_400_BAD_REQUEST)
            guess_letter = guess.validated_data.get("guess")
            current_game = self.get_object()
            updated_game = HangmanService.take_guess(
                guess_letter=guess_letter, game=current_game
            )
            serializer = self.get_serializer(updated_game)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except HangmanService.LetterAlreadyGuessed:
            return Response(
                {"message": "you already guessed this letter."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            return Response(
                {
                    "message": "There was an error processing the guess. Please try again later."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
