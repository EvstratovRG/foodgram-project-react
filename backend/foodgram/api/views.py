from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from recipes.models import Recipe, Tag, Ingredient
from .serializers import RecipeSerializer, TagSerializer, IngredientSerializer


class TagModelViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """Представление CRUD для модели Тэг."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeModelViewSet(ModelViewSet):
    """Представление CRUD для модели Рецепта."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class IngredientModelViewSet(ModelViewSet):
    """Представление CRUD для модели Ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

