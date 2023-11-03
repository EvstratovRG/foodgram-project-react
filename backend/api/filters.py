from rest_framework import filters
from django_filters.rest_framework import FilterSet, filters as filter

from recipes.models import Tag, Recipe


class IngredientFilter(filters.SearchFilter):
    search_param = 'name'


class TagFilter(FilterSet):
    tags = filter.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)
