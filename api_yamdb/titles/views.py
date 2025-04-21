from rest_framework import pagination, viewsets
from rest_framework.permissions import AllowAny
from django.db.models import Avg

from .filters import TitleFilter
from .models import Category, Genre, Title
from api.views import CreateListDestroyViewSet
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, TitleGETSerializer)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]


class TitleViewSet(viewsets.ModelViewSet):
    # todo исправить, когда будет добавлена модель review
    queryset = Title.objects.annotate(rating=Avg('year'))
    # todo включить пермишены
    permission_classes = [AllowAny]
    pagination_class = pagination.LimitOffsetPagination
    filterset_class = TitleFilter
    filterset_fields = ('name',)
    ordering = ('name',)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleGETSerializer
        return TitleSerializer
