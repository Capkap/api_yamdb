from django.urls import path, include
from rest_framework_nested import routers
from rest_framework.authtoken.views import obtain_auth_token
from .views import ReviewViewSet, CommentViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')

comments_router = routers.NestedSimpleRouter(
    router, 
    r'titles/(?P<title_id>\d+)/reviews', 
    lookup='review'
)
comments_router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('api-token-auth/', obtain_auth_token),
    path('v1/', include(router.urls)),
    path('v1/', include(comments_router.urls)),
]
