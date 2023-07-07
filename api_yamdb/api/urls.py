from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, GenreViewSet,
                    MyUserViewSet, TitleViewSet,
                    ReviewViewSet, CommentViewSet,
                    get_token, sign_up)

router = routers.DefaultRouter()

router.register('users', MyUserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', sign_up, name='sign_up'),
    path('v1/auth/token/', get_token, name='get_token')
]
