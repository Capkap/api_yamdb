from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleGETSerializer, TitleSerializer)
from api.views import CreateListDestroyViewSet
from django.db.models import Avg
from rest_framework import pagination, viewsets
from users.permissions import IsAdminOrReadOnly

from .filters import TitleFilter
from .models import Category, Genre, Title


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = pagination.LimitOffsetPagination
    filterset_class = TitleFilter
    filterset_fields = ('name',)
    ordering = ('name',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleSerializer
