import django_filters

from api.models import Score, Project


class ScoreFilters(django_filters.FilterSet):
    filter = django_filters.CharFilter(field_name='game__slug', lookup_expr='icontains')

    class Meta:
        model = Score
        fields = ['game__slug']


class ProjectFilters(django_filters.FilterSet):
    language = django_filters.CharFilter(field_name='language', lookup_expr='icontains')

    class Meta:
        model = Project
        fields = ['language']
