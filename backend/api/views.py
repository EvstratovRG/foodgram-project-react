from typing import Self

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from recipes.models import (
    Recipe,
    Tag,
    Ingredient,
    RecipeIngredient,
    Follow,
    Favorite,
    Purchase,
)
from .permissions import OnlyRead, Author
from .serializers import (
    RecipeSerializer,
    TagSerializer,
    IngredientSerializer,
    GetUserSerializer,

    NotDetailRecipeSerializer,
    FollowSerializer, CreateRecipeSerializer,
)
from .pagination import Pagination
from django.http import HttpResponse
from rest_framework import filters


User = get_user_model()


class UserModelViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """Представление базовой модели User."""
    queryset = User.objects.all()
    serializer_class = GetUserSerializer
    pagination_class = Pagination

    @action(
            detail=False,
            methods=['get'],
            url_path='subscriptions',
            permission_classes=[IsAuthenticated],
        )
    def subscriptions(self: Self, request: Request):
        user = request.user
        subscriptions = User.objects.filter(following__user=user)
        page = self.paginate_queryset(subscriptions)
        serializer = FollowSerializer(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
            detail=True,
            methods=['post', 'delete'],
            url_path='subscribe',
            permission_classes=[IsAuthenticated],
        )
    def subscribe(self: Self, request: Request, pk: int):
        following = self.get_object()
        user = request.user
        if user == following:
            return Response(
                {'detail': 'Нельзя подписываться на самого себя.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        follow = following.following.filter(user=user)
        serializer = FollowSerializer(
            following,
            context={'request': request}
        )
        if follow and request.method == 'DELETE':
            follow.delete()
            return Response(
                {'detail': 'Подписка успешно удалена.'},
                status=status.HTTP_204_NO_CONTENT
            )
        elif not follow and request.method == 'POST':
            Follow.objects.create(
                user=user,
                following=following,
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {'error': 'Ошибка подписки'},
                status=status.HTTP_400_BAD_REQUEST,
            )


class TagModelViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """Представление CRUD для модели Тэг."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (OnlyRead | IsAdminUser,)


class IngredientModelViewSet(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin
):
    """Представление CRUD для модели Ингредиентов."""

    class IngredientFilter(filters.SearchFilter):
        search_param = 'name'
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class RecipeModelViewSet(ModelViewSet):
    """Представление CRUD для модели Рецепта."""

    queryset = Recipe.objects.all().prefetch_related(
        'tags', 'ingredients').select_related(
                'author')
    serializer_class = RecipeSerializer
    pagination_class = Pagination
    permission_classes = (OnlyRead | Author | IsAdminUser,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('tags__slug', 'author')

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated:
            if self.request.query_params.get('is_favorited') == '1':
                queryset = queryset.filter(favorites__user=user)
            if self.request.query_params.get('is_in_shopping_cart') == '1':
                queryset = queryset.filter(purchases__user=user)
        return queryset

    def get_serializer_class(self):
        """Выбирает сериализатор в зависимости от хттп метода."""
        if self.action == 'list':
            return RecipeSerializer
        return CreateRecipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    @action(
            detail=True,
            methods=['post', 'delete'],
            url_path='favorite',
            permission_classes=(IsAuthenticated,),
        )
    def favorite(self: Self, request: Request, pk: int):
        recipe = self.get_object()
        user = request.user
        favor = recipe.favorites.filter(user=user)
        serializer = NotDetailRecipeSerializer(recipe)
        if favor and request.method == 'DELETE':
            favor.delete()
            return Response(
                {'detail': 'Рецепт успешно удален из избранного.'},
                status=status.HTTP_204_NO_CONTENT
            )
        elif not favor and request.method == 'POST':
            Favorite.objects.create(
                user=user,
                recipes=recipe,
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {'error': 'Такого рецепта не существует'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
            detail=True,
            methods=['post', 'delete'],
            url_path='shopping_cart',
            permission_classes=(IsAuthenticated,),
        )
    def shopping_cart(self: Self, request: Request, pk: int):
        recipe = self.get_object()
        user = request.user
        purchase = recipe.purchases.filter(user=user)
        serializer = NotDetailRecipeSerializer(recipe)
        if purchase and request.method == 'DELETE':
            purchase.delete()
            return Response(
                {'detail': 'Рецепт успешно удален из списка покупок.'},
                status=status.HTTP_204_NO_CONTENT
            )
        elif not purchase and request.method == 'POST':
            Purchase.objects.create(
                user=user,
                recipes=recipe,
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {'error': (
                    'Ошибка добавления/удаления рецепта из списка покупок.'
                ),
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
            detail=False,
            methods=['get'],
            url_path='download_shopping_cart',
            permission_classes=(IsAuthenticated, Author,),
        )
    def download_shopping_cart(self: Self, request: Request):
        user = request.user
        cart_data = RecipeIngredient.objects.filter(
            recipes__purchases__user=user
        ).select_related('ingredients')
        if not cart_data:
            return Response(
                {'error': 'Корзина пуста.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        lines = []
        for elem in cart_data:
            lines.append(
                [elem.ingredients.name,
                 elem.ingredients.measurement_unit,
                 str(elem.amount)]
            )
        formated_response = []
        for line in lines:
            formated_line = f'{line[0]} ({line[1]}) - {line[2]}\n'
            formated_response.append(formated_line)
        filename = 'список_покупок.txt'
        response = HttpResponse(formated_response, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response
