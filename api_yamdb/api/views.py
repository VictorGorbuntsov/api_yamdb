from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny

from reviews.models import Category, Genre, Title

from . import serializers
from .permissions import Author, IsAdmin, Moderator, OnlyRead


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return (AllowAny(),)
        return (IsAdmin(),)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return (AllowAny(),)
        return (IsAdmin(),)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(Avg('reviews__score')).\
        select_related('category').prefetch_related('genre')
    serializer_class = serializers.TitleSerializer
    permission_classes = (OnlyRead, IsAdmin,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('name', 'year', 'category__slug', 'genre__slug',)
    ordering_fields = ['name', 'year']

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return serializers.TitleCreateAndUpdateSerializer
        return serializers.TitleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        genre_slug = self.request.query_params.get('genre')
        category_slug = self.request.query_params.get('category')
        if genre_slug:
            queryset = queryset.filter(genre__slug=genre_slug)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset
