from http import HTTPStatus
import secrets

from django.core.mail import send_mail
from django.conf import settings
from rest_framework import views, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.serializers import SignUpSerializer, TokenSerializer, UserSerializer
from users.models import User
from users.permissions import IsAdmin


class SignUpView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        existing_email_user = User.objects.filter(email=email).first()
        existing_username_user = User.objects.filter(username=username).first()
        if existing_email_user and existing_email_user.username != username:
            return Response(
                {'email': 'Этот email уже используется другим пользователем!'},
                status=HTTPStatus.BAD_REQUEST
            )
        if existing_username_user and existing_username_user.email != email:
            return Response(
                {'username': 'Этот username уже занят!'},
                status=HTTPStatus.BAD_REQUEST
            )
        if existing_email_user or existing_username_user:
            user = existing_email_user or existing_username_user
            user.confirmation_code = secrets.token_hex(6)
            user.save()
        else:
            user = User.objects.create(
                email=email,
                username=username,
                confirmation_code=secrets.token_hex(6)
            )
        send_mail(
            subject='Ваш код подтверждения YAmdb!',
            message=f'Ваш код подтверждения: {user.confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response(serializer.data, status=HTTPStatus.OK)


class TokenObtainView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(
                username=serializer.validated_data['username']
            )
        except User.DoesNotExist:
            return Response(
                {'error': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND
            )

        if user.confirmation_code != serializer.validated_data[
            'confirmation_code'
        ]:
            return Response(
                {'error': 'Неверный код подтверждения!'},
                status=HTTPStatus.BAD_REQUEST
            )

        token = str(AccessToken.for_user(user))
        return Response({'token': token}, status=HTTPStatus.OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(username__icontains=search)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role)
            return Response(serializer.data, status=HTTPStatus.OK)

        serializer = self.get_serializer(user)
        return Response(serializer.data, status=HTTPStatus.OK)
