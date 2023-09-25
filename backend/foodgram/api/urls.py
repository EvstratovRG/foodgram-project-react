from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register(r'recipes', views.RecipeModelViewSet, basename='recipes')
router.register(r'tags', views.TagModelViewSet, basename='tags')
router.register(r'ingredients', views.IngredientModelViewSet, basename='ingredients')
router.register(r'users', views.UserModelViewSet, basename='base_users')

urlpatterns = [
    re_path(
    r'^users/subscriptions/$', views.UserModelViewSet.as_view(
        {'get': 'subscriptions'},
        ),
        name='user_subscriptions'
    ),
    re_path(
        r'^users/(?P<pk>\d+)/subscribe/$', 
        views.UserModelViewSet.as_view(
            {'post': 'subscribe'}
        ), 
        name='user_subscribe'
    ),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]


# router.register(
#     r'recipes/(?<recipe_id>\d+)/favorites/',
#     views.RecipeModelViewSet,
#     basename='favorites'
# )
# router.register(
#     r'recipes/(?<recipe_id>\d+)/download_shopping_cart/',
#     views.RecipeModelViewSet,
#     basename='download_shopping_cart'
# )
# router.register(
#     r'recipes/(?<recipe_id>\d+)/shopping_cart/',
#     views.RecipeModelViewSet,
#     basename='shopping_cart'
# )
