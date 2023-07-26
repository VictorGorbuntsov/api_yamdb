from rest_framework import filters, mixins, viewsets

from .permissions import IsAdmin, OnlyRead


class ListDestroyCreateWithFilters(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin
):
    """Класс представлений ListDestroyCreate с применением фильтрации."""
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (OnlyRead | IsAdmin,)
