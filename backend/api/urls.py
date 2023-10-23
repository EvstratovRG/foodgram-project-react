from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'recipes', views.RecipeModelViewSet)

router.register(r'tags', views.TagModelViewSet)
router.register(r'ingredients', views.IngredientModelViewSet)
router.register(r'users', views.UserModelViewSet, basename='users')
router.register(
    r'recipes/(?P<recipe_pk>\d+)/favorite',
    views.RecipeModelViewSet,
    basename='favorite',
)
router.register(
    r'users/(?P<user_pk>\d+)/subscribe',
    views.UserModelViewSet,
    basename='subscribe',
)

router.register(
    r'recipes/download_shopping_cart',
    views.RecipeModelViewSet,
    basename='download-shopping-cart',
)

router.register(
    r'recipes/(?P<recipe_pk>\d+)/shopping_cart',
    views.RecipeModelViewSet,
    basename='shopping-cart',
)
# router.register(
#     r'users/(?P<user_pk>\d+)/subscribe/$',
#     views.UserModelViewSet, basename='subscribe'
# )
# router.register(r'users/subscriptions', views.UserModelViewSet, basename='user_subscriptions')
# router.register(
#         r'recipes/(?P<recipe_pk>\d+)/favorite/',
#         views.RecipeModelViewSet,
#         basename='favorite',
#     )
# router.register(
#         r'recipes/download_shopping_cart/',
#         views.RecipeModelViewSet,
#         basename='download_shopping_cart',
#     )
# router.register(
#         r'recipes/(?P<recipe_pk>\d+)/shopping_cart/',
#         views.RecipeModelViewSet,
#         basename='shopping_cart',
#     )


urlpatterns = [
    re_path(
        r'^users/subscriptions/$', views.UserModelViewSet.as_view(
            {'get': 'subscriptions'},
        ),
        name='user_subscriptions'
    ),

    # re_path(
    #     r'recipes/(?P<pk>\d+)/favorite/',
    #     views.RecipeModelViewSet.as_view({'post': 'favorite'}),
    #     name='favorite',
    # ),
    # re_path(
    #     r'recipes/(?P<pk>\d+)/download_shopping_cart/',
    #     views.RecipeModelViewSet.as_view({'get': 'download_shopping_cart'}),
    #     name='download_shopping_cart',
    # ),
    # re_path(
    #     r'recipes/(?P<pk>\d+)/shopping_cart/',
    #     views.RecipeModelViewSet.as_view({'post': 'shopping_cart'}),
    #     name='shopping_cart',
    # ),
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
