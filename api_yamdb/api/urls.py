from rest_framework.routers import DefaultRouter
from django.urls import include, path


urlpatterns = [
    path('v1/', include('titles.urls')),
]
