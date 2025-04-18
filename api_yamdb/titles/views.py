from rest_framework import pagination, viewsets
from django.db.models import Avg

from .filters import TitleFilter
from .models import Category, Genre, Title
from api.views import CreateListDestroyViewSet
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, TitleGETSerializer)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    # todo исправить, когда будет добавлена модель review
    queryset = Title.objects.annotate(rating=Avg('year'))
    # todo включить пермишены
    # permission_classes = ()
    pagination_class = pagination.LimitOffsetPagination
    filterset_class = TitleFilter
    filterset_fields = ('name',)
    ordering = ('name',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleSerializer
