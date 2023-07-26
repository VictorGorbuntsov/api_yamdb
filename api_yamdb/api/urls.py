from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .constants import URL_COMMENTS, URL_REVIEW
from .views import (CategoryViewSet, CommentViewSet, CustomUserViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet, get_token,
                    sign_up)


router = SimpleRouter()

router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(URL_COMMENTS, CommentViewSet, basename='comment')
router.register(URL_REVIEW, ReviewViewSet, basename='review')

auth_patterns = [
    path('signup/', sign_up, name='sign_up'),
    path('token/', get_token, name='get_token'),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_patterns)),
]
