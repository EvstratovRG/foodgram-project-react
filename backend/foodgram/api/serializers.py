from djoser import serializers as djoser_serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from recipes.models import Recipe


User = get_user_model()


class DjoserUserCreateSerializer(djoser_serializers.UserCreateSerializer):
    class Meta(djoser_serializers.UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password')


class GetUserSerializer(serializers.ModelSerializer):

    # is_subscribed = serializers.BooleanField() подписан ли текущий пользователь на этого

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели Рецепт."""
    class Meta:
        model = Recipe
        fields = '__all__'
