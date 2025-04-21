from http import HTTPStatus

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from api.serializers import SignUpSerializer, TokenSerializer


class SignUpView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        user, created = User.objects.get_or_create(
            email=email,
            username=username
        )
        confirmation_code = user.generate_confirmation_code()
        send_mail(
            subject='Ваш личный код подтверждения YAmdb',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response(
            serializer.data,
            status=HTTPStatus.OK
        )


class TokenObtainView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        if user.confirmation_code != serializer.validated_data[
            'confirmation_code'
        ]:
            return Response(
                {'error': 'Неверный код подтверждения'},
                status=HTTPStatus.BAD_REQUEST
            )
        token = str(AccessToken.for_user(user))
        return Response(
            {'token': token},
            status=HTTPStatus.OK
        )
