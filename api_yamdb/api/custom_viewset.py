from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.viewsets import GenericViewSet


class CreateListDestroyModelViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
    ListModelMixin,
):
    """Mixin for create, list and destroy methods."""

    filter_backends = (SearchFilter,)
    search_fields = ('name',)
