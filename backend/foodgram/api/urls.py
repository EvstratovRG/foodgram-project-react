from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()

router.register(r'recipes', views.RecipeModelViewSet)
router.register(r'tags', views.TagModelViewSet)
router.register(r'ingredients', views.IngredientModelViewSet)


urlpatterns = [
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
