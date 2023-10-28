from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'users', views.UserModelViewSet, basename='users')
router.register(
    r'users/(?P<user_pk>\d+)/subscribe',
    views.UserModelViewSet,
    basename='subscribe',
)
router.register(r'recipes', views.RecipeModelViewSet)
router.register(
    r'recipes/(?P<recipe_pk>\d+)/shopping_cart',
    views.RecipeModelViewSet,
    basename='shopping-cart',
)
router.register(
    r'recipes/(?P<recipe_pk>\d+)/favorite',
    views.RecipeModelViewSet,
    basename='favorite',
)
router.register(r'tags', views.TagModelViewSet)
router.register(r'ingredients', views.IngredientModelViewSet)


urlpatterns = [
    re_path(
        r'^users/subscriptions/$', views.UserModelViewSet.as_view(
            {'get': 'subscriptions'},
        ),
        name='user_subscriptions'
    ),
    re_path(
        r'recipes/download_shopping_cart/',
        views.RecipeModelViewSet.as_view({'get': 'download_shopping_cart'}),
        name='download_shopping_cart',
    ),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
