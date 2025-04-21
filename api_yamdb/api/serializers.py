import datetime as dt
import re

from rest_framework import serializers
from django.core.exceptions import ValidationError
from rest_framework import serializers

from titles.models import Category, Genre, Title
from users.models import User


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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


class TitleGETSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(default=0)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        read_only_fields = (
            'rating',
            'genre',
            'category'
        )


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=True,
        allow_empty=False
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'name',
            'year',
            'description',
            'genre',
            'category'
        )

    @staticmethod
    def validate_year(value):
        if value > dt.date.today().year:
            raise serializers.ValidationError(
                'Год произведения не может быть больше текущего.'
            )
        return value

    @staticmethod
    def to_representation(title):
        return TitleGETSerializer(title).data
