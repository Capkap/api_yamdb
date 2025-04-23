from django.urls import include, path

urlpatterns = [
    path('v1/', include('titles.urls')),
    path('v1/', include('users.urls')),
    path('v1/', include('reviews.urls')),
]
