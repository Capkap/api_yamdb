from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
from .models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer
from api.permissions import (AuthorModeratorAdminOrSafeMethodOnly)


class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorModeratorAdminOrSafeMethodOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewUpdate(generics.RetrieveUpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorModeratorAdminOrSafeMethodOnly,)

    def perform_update(self, serializer):
        serializer.save()


class ReviewDestroy(generics.RetrieveDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorModeratorAdminOrSafeMethodOnly,)


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorModeratorAdminOrSafeMethodOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentUpdate(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorModeratorAdminOrSafeMethodOnly,)

    def perform_update(self, serializer):
        serializer.save()


class CommentDestroy(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthorModeratorAdminOrSafeMethodOnly,)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'review': reverse('review-list', request=request, format=format),
        'comment': reverse('comment-list', request=request, format=format)
    })
