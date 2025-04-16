from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    ReviewList, ReviewUpdate, ReviewDestroy,
    CommentList, CommentUpdate, CommentDestroy
)

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewList,
    basename='reviews'
)

router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentList,
    basename='comments'
)

urlpatterns = [
    path('v1/api-token-auth/', obtain_auth_token),
    path('v1/', include(router_v1.urls)),

    # URL для обновления/удаления отзывов
    path(
        'v1/titles/(?P<title_id>\d+)/reviews/(?P<pk>\d+)/',
        ReviewUpdate.as_view(),
        name='review-detail'
    ),
    path(
        'v1/titles/(?P<title_id>\d+)/reviews/(?P<pk>\d+)/',
        ReviewDestroy.as_view(),
        name='review-delete'
    ),

    # URL для обновления/удаления комментариев
    path(
        'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/(?P<pk>\d+)/',
        CommentUpdate.as_view(),
        name='comment-detail'
    ),
    path(
        'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/(?P<pk>\d+)/',
        CommentDestroy.as_view(),
        name='comment-delete'
    )
]
