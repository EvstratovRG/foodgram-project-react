from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import (
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin,
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from recipes.models import Recipe, Tag, Ingredient, RecipeIngredients, Follow
from .serializers import (
    RecipeSerializer,
    TagSerializer,
    IngredientSerializer,
    GetUserSerializer,
    RecipeIngredientSerializer, FollowSerializer,
)


User = get_user_model()


class UserModelViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """Представление базовой модели User."""
    queryset = User.objects.all()
    serializer_class = GetUserSerializer
    pagination_class = LimitOffsetPagination

    @action(detail=False, methods=['get'], url_path='subscriptions')
    def subscriptions(self, request):
        user = request.user
        subscriptions = user.following.all()
        serializer = FollowSerializer(subscriptions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='subscribe')
    def subscribe(self, request, pk=None):
        user_to_subscribe_or_unsubscribe = self.get_object()
        user = request.user
        if user == user_to_subscribe_or_unsubscribe:
            return Response(
                {'detail': 'Вы не можете подписаться на самого себя.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        follow = user_to_subscribe_or_unsubscribe.followers.filter(user=user).first()

        if follow:
            follow.delete()
            return Response(
                {'detail': 'Подписка успешно удалена.'}, 
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            Follow.objects.create(
                user=user, 
                following=user_to_subscribe_or_unsubscribe,
            )
            return Response(
                {'detail': 'Подписка успешно создана.'}, 
                status=status.HTTP_201_CREATED,
            )


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
