from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register(r'recipes', views.RecipeModelViewSet, basename='recipes')
router.register(r'tags', views.TagModelViewSet, basename='tags')
router.register(r'ingredients', views.IngredientModelViewSet, basename='ingredients')


urlpatterns = [
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
