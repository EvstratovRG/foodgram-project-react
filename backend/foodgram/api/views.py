from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters, status
from django.contrib.auth import get_user_model

from recipes.models import Recipe, Tag, Ingredient, RecipeIngredients
from .serializers import (
    RecipeSerializer,
    TagSerializer,
    IngredientSerializer,
    GetUserSerializer,
    RecipeIngredientSerializer
)


User = get_user_model()


class UserModelViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """Представление базовой модели User."""
    queryset = User.objects.all()
    serializer_class = GetUserSerializer
    pagination_class = LimitOffsetPagination
    # не работает лимитофсет на юзере


class TagModelViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """Представление CRUD для модели Тэг."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientModelViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """Представление CRUD для модели Ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class RecipeModelViewSet(ModelViewSet):
    """Представление CRUD для модели Рецепта."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeIngredientsModelViewSet(ModelViewSet):
    """Представление для Рецепт-ингредиенты."""

    queryset = RecipeIngredients.objects.all()
    serializer_class = RecipeIngredientSerializer
