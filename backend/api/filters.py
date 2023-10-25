from rest_framework import filters as search_filter
from django_filters.rest_framework import FilterSet, filters

from recipes.models import Tag, Recipe


class IngredientFilter(search_filter.SearchFilter):
    search_param = 'name'


class RecipeFilter(search_filter.BaseFilterBackend):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited'
    )
    print(is_favorited)
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)

    def filter_is_favorited(self, queryset, value):
        user = self.request.user
        print('тут должно быть вэлью')
        print(value)
        if value:
            print(queryset.filter(favorites__user=user))
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, value):
        user = self.request.user
        print(value)
        if value:
            return queryset.filter(purchases__user=user)
        return queryset
