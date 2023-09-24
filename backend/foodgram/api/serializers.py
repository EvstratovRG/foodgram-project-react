import base64
import webcolors

from django.core.files.base import ContentFile
from djoser import serializers as djoser_serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Recipe, Tag, Ingredient, RecipeIngredients, Follow


User = get_user_model()


class DjoserUserCreateSerializer(djoser_serializers.UserCreateSerializer):

    class Meta(djoser_serializers.UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password')


class GetUserSerializer(serializers.ModelSerializer):

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


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор модели Ингредиент."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Связующий сериализатор рецептов и количества ингредиентов."""

    class Meta:
        model = RecipeIngredients
        fields = ('id', 'amount',)


class TagIDSerializer(serializers.ModelSerializer):
    """Сериализатор модели Тэг."""

    class Meta:
        model = Tag
        fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели Рецепт."""

    tags = TagIDSerializer(many=True)
    author = GetUserSerializer(required=True)
    ingredients = RecipeIngredientSerializer(many=True)
    image = Base64ImageFieldSerializer(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'name',
            'image',
            'text',
            'ingredients',
            'tags',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def create(self, validated_data):
        if 'ingredients' not in self.initial_data: # type: ignore
            recipe = Recipe.objects.create(**validated_data)
            return recipe
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            amount = ingredient_data.pop('amount', None)
            current_ingredient, _ = Ingredient.objects.get_or_create(
                **ingredient_data
            )
            RecipeIngredients.objects.create(
                ingredient=current_ingredient, recipe=recipe, amount=amount,
            )
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        instance.is_favorited = validated_data.get('is_favorited', instance.is_favorited)
        instance.is_in_shopping_cart = validated_data.get('is_in_shopping_cart', instance.is_in_shopping_cart)

        if 'ingredients' not in validated_data:
            instance.save()
            return instance
    
        ingredients_data = validated_data.pop('ingredients')
        instance.ingredients.clear()
        for ingredient_data in ingredients_data:
            amount = ingredient_data.pop('amount', None)
            current_ingredient, _ = Ingredient.objects.get_or_create(**ingredient_data)
            RecipeIngredients.objects.create(ingredient=current_ingredient, recipe=instance, amount=amount)

        instance.save()
        return instance
