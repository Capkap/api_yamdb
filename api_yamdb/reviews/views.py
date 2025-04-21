from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from users.permissions import IsAuthorModeratorAdminOrReadOnly
from api.serializers import ReviewSerializer, CommentSerializer
from .models import Review, Comment
from titles.models import Title


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с отзывами (Reviews)."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_queryset(self):
        return Review.objects.select_related('author').filter(
            title_id=self.kwargs['title_id'])

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с комментариями к отзывам."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.select_related('author', 'review').filter(
            review_id=self.kwargs['review_id'])

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(
            author=self.request.user,
            review=review
        )
