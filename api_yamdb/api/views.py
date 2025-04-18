from rest_framework import pagination, viewsets, mixins
from rest_framework.filters import SearchFilter


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    # todo включить пермишены
    # permission_classes = ()
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
