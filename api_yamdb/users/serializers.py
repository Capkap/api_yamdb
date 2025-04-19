import re

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(required=True, max_length=150)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise ValidationError("Нельзя использовать 'me' как username!")

        if not re.match(r'^[\w.@+-]+\Z', value):
            raise ValidationError("В username есть допустимые символы!")

        return value

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise ValidationError(
                {'email': 'Email уже используется для другого аккаунта!'}
            )

        if User.objects.filter(username=data['username']).exists():
            raise ValidationError({'username': 'Такой username уже занят!'})

        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise ValidationError({'username': 'Пользователь не найден!'})

        if user.confirmation_code != data['confirmation_code']:
            raise ValidationError(
                {'confirmation_code': 'Неверный код подтверждения!'}
            )

        return data
