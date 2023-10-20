from typing import Self

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from recipes.models import Recipe, Tag, Ingredient, RecipeIngredient, Follow, Favorite, Purchase  # type: ignore
from .permissions import OnlyRead, Author

from .exceptions import SelfFollowException
from .serializers import (
    RecipeSerializer,
    TagSerializer,
    IngredientSerializer,
    GetUserSerializer,
    RecipeIngredientSerializer,
    NotDetailRecipeSerializer,
    FollowSerializer, CreateRecipeSerializer,
)


User = get_user_model()


class IngredientFilter(filters.SearchFilter):
    search_param = 'name'


class UserModelViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """Представление базовой модели User."""
    queryset = User.objects.all()
    serializer_class = GetUserSerializer
    pagination_class = LimitOffsetPagination

    @action(detail=False, methods=['get'], url_path='subscriptions', permission_classes=[IsAuthenticated])
    def subscriptions(self: Self, request: Request):
        user = request.user
        subscriptions = user.follower.all().select_related('following')
        serializer = FollowSerializer(
            [follow.following for follow in subscriptions],
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='subscribe', permission_classes=[IsAuthenticated])
    def subscribe(self: Self, request: Request, pk: int):
        user_to_subscribe_or_unsubscribe = self.get_object()
        user = request.user
        if user == user_to_subscribe_or_unsubscribe:
            return Response(
                {'detail': SelfFollowException},
                status=status.HTTP_400_BAD_REQUEST
            )
        follow = user_to_subscribe_or_unsubscribe.following.filter(user=user)

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
    permission_classes = (OnlyRead | IsAdminUser,)


class IngredientModelViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """Представление CRUD для модели Ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class RecipeModelViewSet(ModelViewSet):
    """Представление CRUD для модели Рецепта."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (OnlyRead | Author | IsAdminUser,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('is_favorited', 'author', 'tags__name', 'is_in_shopping_cart',)

    def get_serializer_class(self):
        """Выбирает сериализатор в зависимости от хттп метода."""
        if self.action == 'list':
            return RecipeSerializer
        return CreateRecipeSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    # def create(self, request, *args, **kwargs):
    #     serializer = CreateRecipeSerializer(data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save(author=self.request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='favorite', permission_classes=[IsAuthenticated])
    def favorite(self: Self, request: Request, pk: int):
        recipe = self.get_object()
        user = request.user
        favor = recipe.favorites.filter(user=user)
        serializer = NotDetailRecipeSerializer(
            recipe,
            context={'request': request})
        if favor:
            favor.delete()
            return Response(
                {'detail': 'Рецепт удален из избранных.'},
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            Favorite.objects.create(
                user=user,
                recipes=recipe,
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

    @action(detail=False, methods=['post'], url_path='shopping_cart', permission_classes=[IsAuthenticated])
    def shopping_cart(self: Self, request: Request, pk: int):
        recipe = self.get_object()
        user = request.user
        purchase = recipe.purchases.filter(user=user)
        serializer = NotDetailRecipeSerializer(
            recipe,
            context={'request': request})
        if purchase:
            purchase.delete()
            return Response(
                {'detail': 'Рецепт удален из списка покупок.'},
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            Purchase.objects.create(
                user=user,
                recipes=recipe,
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

    @action(detail=False, methods=['get'], url_path='download_shopping_cart', permission_classes=[IsAuthenticated])
    def download_shopping_cart(self: Self, request: Request):
        user = request.user
        cart_data = RecipeIngredient.objects.filter(
            recipes__purchases__user=user
        ).select_related('ingredients')
        buffer = io.BytesIO()
        canvas_obj = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
        text_operation = canvas_obj.beginText()
        text_operation.setTextOrigin(inch, inch)
        text_operation.setFont("Helvetica", 14)
        lines = []
        for elem in cart_data:
            lines.extend([elem.recipes.name, elem.ingredients.name, str(elem.amount)])
        print(lines)
        for line in lines:
            text_operation.textLine(line)
        canvas_obj.drawText(text_operation)
        canvas_obj.showPage()
        canvas_obj.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='cart_data.pdf')


class RecipeIngredientModelViewSet(ModelViewSet):
    """Представление для Рецепт-ингредиенты."""

    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer
