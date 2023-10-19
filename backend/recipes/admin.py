from django.contrib import admin

from .models import (
    Follow,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Tag,
    Purchase,
    Favorite,
    RecipeTag,
)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'following']
    list_filter = ['user', 'following']
    search_fields = ['user__email', 'user__username', 'following__email', 'following__username']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'measurement_unit', 'created_at', 'updated_at']
    list_filter = ['name', 'measurement_unit']
    search_fields = ['name']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'author',
        'get_tags_names',
        'get_ingredients_names',
        'cooking_time',
        'favorites_count',
    ]
    list_filter = ['author', 'name', 'tags']
    search_fields = ['name']

    def get_tags_names(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])

    get_tags_names.short_description = 'Tags'

    def get_ingredients_names(self, obj):
        return ', '.join([ingredient.name for ingredient in obj.ingredients.all()])

    get_ingredients_names.short_description = 'Ingredients'

    def favorites_count(self, obj):
        return obj.favorites.count()

    favorites_count.short_description = 'Favorites'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'recipes',
        'ingredients',
        'amount',
        'created_at',
        'updated_at'
    ]
    list_filter = ['recipes', 'ingredients', 'amount']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'color', 'slug', 'created_at', 'updated_at']
    list_filter = ['name', 'color']
    search_fields = ['name']


@admin.register(RecipeTag)
class RecipeTagsAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'recipes',
        'tags',
        'created_at',
        'updated_at'
    ]
    list_filter = ['recipes', 'tags']


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipes', 'created_at', 'updated_at']
    list_filter = ['user', 'recipes']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipes', 'created_at', 'updated_at']
    list_filter = ['user', 'recipes']
    search_fields = ['user__email', 'user__username']
