from django.db.models import Avg
from rest_framework import pagination, viewsets

from api.filters import TitleFilter
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleGETSerializer, TitleSerializer)
from api.views import CreateListDestroyViewSet
from users.permissions import IsAdminOrReadOnly

from .models import Category, Genre, Title


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')
                                      ).order_by('-id')
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
