from rest_framework.viewsets import ModelViewSet

from recipes.models import Recipe
from .serializers import RecipeSerializer


class RecipeModelViewSet(ModelViewSet):
    """Представление CRUD для модели Рецепта."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer()
