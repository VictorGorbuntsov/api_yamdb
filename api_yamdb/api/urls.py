from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, GenreViewSet, MyUserViewSet, TitleViewSet,
                    get_token, sign_up)

router = routers.DefaultRouter()

router.register('users', MyUserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', sign_up, name='sign_up'),
    path('v1/auth/token/', get_token, name='get_token')
]
