from django.urls import path
from .views import SignUpView, TokenObtainView

urlpatterns = [
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('auth/token/', TokenObtainView.as_view(), name='token'),
]
