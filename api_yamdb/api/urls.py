from .views import (CategoryViewSet, CommentsViewSet, GenreViewSet,
                    ReviewsViewSet, TitleViewSet)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('titles', TitleViewSet, 'Title')
router.register('categories', CategoryViewSet, 'Category')
router.register('genres', GenreViewSet, 'Genre')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
