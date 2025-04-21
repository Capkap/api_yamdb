from django.urls import include, path

from django.urls import path, include

urlpatterns = [
    path('v1/', include('titles.urls')),
    path('v1/', include('users.urls')),
  path('v1/', include('reviews.urls')),
]

