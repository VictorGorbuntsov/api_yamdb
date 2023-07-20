from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .constants import URL_COMMENTS, URL_REVIEW
from .views import (CategoryViewSet, GenreViewSet,
                    MyUserViewSet, TitleViewSet,
                    ReviewViewSet, CommentViewSet,
                    get_token, sign_up)

prefix = 'v1/'
auth_prefix = prefix + 'auth/'
router = SimpleRouter()

router.register(r'users', MyUserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(URL_COMMENTS, CommentViewSet, basename='comment')
router.register(URL_REVIEW, ReviewViewSet, basename='review')


urlpatterns = [
    path(prefix, include(router.urls)),
    path(auth_prefix + 'signup/', sign_up, name='sign_up'),
    path(auth_prefix + 'token/', get_token, name='get_token')
]
