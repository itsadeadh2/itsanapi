from rest_framework import serializers

from api.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "name",
            "description",
            "language",
            "stack",
            "github_link",
            "docs_link",
        ]
        model = Project
