from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include

from titles.views import CategoryViewSet, GenreViewSet, TitleViewSet
from reviews.views import ReviewViewSet, CommentViewSet

app_name = 'api'

# Основной роутер
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')

# Вложенные роутеры для отзывов и комментариев
titles_router = routers.NestedSimpleRouter(
    router, r'titles', lookup='title')
titles_router.register(r'reviews', ReviewViewSet, basename='title-reviews')

reviews_router = routers.NestedSimpleRouter(
    titles_router, r'reviews', lookup='review')

reviews_router.register(
    r'comments', CommentViewSet, basename='review-comments')

urlpatterns = [
    path('api-token-auth/', obtain_auth_token),
    path('v1/', include(router.urls)),
    path('v1/', include(titles_router.urls)),
    path('v1/', include(reviews_router.urls)),
]
