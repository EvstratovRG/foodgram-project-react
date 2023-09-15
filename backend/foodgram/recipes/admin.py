from django.contrib import admin

from .models import Follow, Ingredient, Recipe, RecipeTag, Tag 


admin.site.register(Follow)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeTag)
admin.site.register(Tag)
