from rest_framework import serializers


class GuessSerializer(serializers.Serializer):
    guess = serializers.CharField(max_length=1)
