from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime as dt
import re

from reviews.models import Review, Comment
from users.models import User
from titles.models import Category, Genre, Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализации объектов модели Review."""
    author = serializers.CharField(source='author.username', read_only=True)
    pub_date = serializers.DateTimeField(read_only=True)
    score = serializers.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        error_messages={
            'min_value': 'Минимальная оценка 1',
            'max_value': 'Максимальная оценка 10'
        }
    )
    title = serializers.IntegerField(source='title.id')

    def validate(self, attrs):
        if self.context['request'].method == 'POST':
            title_id = attrs['title']
            user = self.context['request'].user
            if Review.objects.filter(title_id=title_id, author=user).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв на это произведение'
                )
        return attrs

    class Meta:
        model = Review
        fields = ('id', 'title', 'text', 'score', 'author', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализации вложенных комментариев к отзыву."""
    author = serializers.CharField(source='author.username', read_only=True)
    review = serializers.IntegerField(source='review.id')

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author')


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
    """Сериализатор для получения JWT-токена."""
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
