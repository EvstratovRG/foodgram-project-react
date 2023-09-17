from django.contrib import admin

from .models import (
    Follow, 
    Ingredient, 
    Recipe, 
    RecipeIngredients, 
    Tag, 
    Purchase,
)


admin.site.register(Follow)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredients)
admin.site.register(Tag)
admin.site.register(Purchase)
