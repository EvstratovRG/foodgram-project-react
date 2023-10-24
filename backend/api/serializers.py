import base64
import webcolors

from django.core.files.base import ContentFile
from django.db import transaction
from djoser import serializers as djoser_serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import (
    Recipe,
    Tag,
    Ingredient,
    RecipeIngredient,
    RecipeTag,
)


User = get_user_model()


class DjoserUserCreateSerializer(djoser_serializers.UserCreateSerializer):
    """Сериализатор для списка пользователя через джосер."""

    class Meta(djoser_serializers.UserCreateSerializer.Meta):
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )


class GetUserSerializer(serializers.ModelSerializer):
    """Общий сериализатор для пользователей."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """Функция получения статуса подписки."""
        if self.context['request'] is None or (
            self.context['request'].user.is_anonymous
        ):
            return False
        current_user = self.context['request'].user
        print(current_user)
        is_subscribed = obj.following.filter(user=current_user).exists()
        return is_subscribed


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

    amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'amount', 'measurement_unit',)

    def get_amount(self, obj):
        recipe_ingredient = obj.recipe_ingredients.first()
        if recipe_ingredient:
            return recipe_ingredient.amount
        else:
            return None


class TagIDSerializer(serializers.ModelSerializer):
    """Сериализатор модели Тэг."""

    class Meta:
        model = Tag
        fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели Рецепт LIST запросы."""

    tags = TagSerializer(many=True)
    author = GetUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(many=True)
    image = Base64ImageFieldSerializer(required=False, allow_null=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

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

    def get_is_favorited(self, obj):
        if self.context['request'] is None or (
            self.context['request'].user.is_anonymous
        ):
            return False
        user = self.context['request'].user
        is_favorited = obj.favorites.filter(user=user).exists()
        return is_favorited

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'] is None or (
            self.context['request'].user.is_anonymous
        ):
            return False
        user = self.context['request'].user
        is_in_shopping_cart = obj.purchases.filter(user=user).exists()
        return is_in_shopping_cart


class CreateIngredientFromRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели Ингредиент."""
    id = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount',)


class CreateRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор модели Рецепт Create, Update, Distroy запросы."""
    ingredients = CreateIngredientFromRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageFieldSerializer()
    author = GetUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def validate_ingredients(self, data):
        ingredients = self.initial_data.get('ingredients')
        ingredients_array = []
        for ingredient in ingredients:
            amount = ingredient['amount']
            if int(amount) < 1:
                raise serializers.ValidationError({
                   'amount': 'Количество не может быть меньше 1'
                })
            if ingredient['id'] in ingredients_array:
                raise serializers.ValidationError({
                   'ingredient': 'Ингредиенты не дублируются'
                })
            ingredients_array.append(ingredient['id'])
        return data

    @transaction.atomic
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        author = self.context.get('request').user
        print(validated_data)
        recipe = Recipe.objects.create(author=author, **validated_data)
        for ingredient_data in ingredients_data:
            amount = ingredient_data['amount']
            ingredient_id = ingredient_data['id']
            RecipeIngredient.objects.create(
                ingredients=Ingredient.objects.get(id=ingredient_id),
                recipes=recipe,
                amount=amount,
            )

        recipe.tags.set(tags_data)
        recipe.save()
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time,
        )
        instance.is_favorited = validated_data.get(
            'is_favorited',
            instance.is_favorited,
        )
        instance.is_in_shopping_cart = validated_data.get(
            'is_in_shopping_cart',
            instance.is_in_shopping_cart,
        )

        if 'ingredients' and 'tags' not in validated_data:
            instance.save()
            return instance

        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        instance.tags.clear()
        instance.ingredients.clear()
        for ingredient_data in ingredients_data:
            amount = ingredient_data.pop('amount', None)
            current_ingredient = Ingredient.objects.get(
                id=ingredient_data['id'],
            )
            RecipeIngredient.objects.create(
                ingredients=current_ingredient,
                recipes=instance,
                amount=amount,
            )
        for tag in tags_data:
            RecipeTag.objects.create(
                tags=tag,
                recipes=instance
            )

        instance.save()
        return instance

    def to_representation(self, instance):
        serializer = RecipeSerializer(
            instance,
            context={'request': self.context.get('request')},
        )
        return serializer.data


class NotDetailRecipeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class FollowSerializer(GetUserSerializer):

    recipes = NotDetailRecipeSerializer(many=True, allow_null=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta(GetUserSerializer.Meta):
        fields = GetUserSerializer.Meta.fields + (
            'recipes',
            'recipes_count',
        )

    def get_recipes_count(self, obj):
        recipe_count = Recipe.objects.filter(author=obj).count()
        return recipe_count
