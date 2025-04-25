from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.serializers import CommentSerializer, ReviewSerializer
from titles.models import Title
from users.permissions import IsAuthorModeratorAdminOrReadOnly
from .models import Review


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с отзывами (Reviews)."""

    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorModeratorAdminOrReadOnly)

    def get_queryset(self):
        return Review.objects.filter(title_id=self.kwargs['title_id'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['title_id'] = self.kwargs['title_id']
        return context

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с комментариями к отзывам."""

    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAuthorModeratorAdminOrReadOnly)

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs['review_id'],
            title_id=self.kwargs['title_id']
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)
