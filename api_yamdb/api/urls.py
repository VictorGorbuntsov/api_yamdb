from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import (CategoryViewSet, GenreViewSet, MyUserViewSet, TitleViewSet,
                    ReviewViewSet, CommentViewSet,
                    get_token, sign_up)

URL_COMMENTS = r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments'
URL_REVIEW = r'titles/(?P<title_id>\d+)/reviews'

router = SimpleRouter()

router.register(r'users', MyUserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(URL_COMMENTS, CommentViewSet, basename='comment')
router.register(URL_REVIEW, ReviewViewSet, basename='review')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', sign_up, name='sign_up'),
    path('v1/auth/token/', get_token, name='get_token')
]
