from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter

from . views import RecipeModelViewSet


router = SimpleRouter()
router.register(r'', RecipeModelViewSet)


urlpatterns = [
    path('', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
