import base64
import webcolors

from django.core.files.base import ContentFile
from djoser import serializers as djoser_serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Recipe, Tag, Ingredient


User = get_user_model()


class DjoserUserCreateSerializer(djoser_serializers.UserCreateSerializer):

    class Meta(djoser_serializers.UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password')


class GetUserSerializer(serializers.ModelSerializer):

    # is_subscribed = serializers.BooleanField() подписан ли текущий пользователь на этого

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',)


class Base64ImageFieldSerializer(serializers.ImageField):
    """Сериализатор изображения в base64."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class Hex2NameColorSerializer(serializers.Field):
    """Сериализатор цвета в хекс формат."""

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели Тэг."""

    color = Hex2NameColorSerializer()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели Рецепт."""

    class Meta:
        model = Recipe
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели Ингредиент."""

    class Meta:
        model = Ingredient
        fields = '__all__'
