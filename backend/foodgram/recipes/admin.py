from django.contrib import admin

from .models import (
    Follow, 
    Ingredient, 
    Recipe, 
    RecipeIngredients, 
    Tag, 
    Purchase,
    Favorite,
)

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'following']
    list_filter = ['user', 'following']
    search_fields = ['user']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'measurement_unit', 'created_at', 'updated_at']
    list_filter = ['name', 'measurement_unit', 'created_at', 'updated_at']
    search_fields = ['name']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'author',
        'name',
        'image',
        'text',
        'get_tags_names',
        'get_ingredients_names',
        'cooking_time',
        'is_favorited',
        'is_in_shopping_cart',
        'created_at',
        'updated_at'
    ]
    list_filter = [
        'author',
        'name',
        'image',
        'text',
        'cooking_time',
        'is_favorited',
        'is_in_shopping_cart',
        'created_at',
        'updated_at'
    ]
    search_fields = ['tags', 'name']

    def get_tags_names(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])
    get_tags_names.short_description = 'Tags'
    
    def get_ingredients_names(self, obj):
        return ', '.join([ingredient.name for ingredient in obj.ingredients.all()])
    get_ingredients_names.short_description = 'Ingredients'


@admin.register(RecipeIngredients)
class RecipeIngredientsAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'recipes', 
        'ingredients',
        'amount', 
        'created_at', 
        'updated_at'
    ]
    list_filter = ['recipes', 'ingredients', 'amount']
    def get_ingredients_names(self, obj):
        return ', '.join([ingredient.name for ingredient in obj.recipeingredients.all()])
    get_ingredients_names.short_description = 'ingredients'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'color', 'slug', 'created_at', 'updated_at']
    list_filter = ['name', 'color', 'slug', 'created_at', 'updated_at']
    search_fields = ['slug']


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipes', 'created_at', 'updated_at']
    list_filter = ['user', 'recipes', 'created_at', 'updated_at']
    search_fields = ['user']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'recipes', 'created_at', 'updated_at']
    list_filter = ['user', 'recipes', 'created_at', 'updated_at']
    search_fields = ['user']
