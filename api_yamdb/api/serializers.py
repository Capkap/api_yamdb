from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from rest_framework import serializers

from api_yamdb import constants
from api.validators import validate_year
from reviews.models import Comment, Review
from titles.models import Category, Genre, Title
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализации объектов модели Review."""
    author = serializers.CharField(source='author.username', read_only=True)
    title = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        write_only=True
    )
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

    def validate(self, data):
        request = self.context['request']
        title_id = self.context['title_id']

        if request.method == 'POST':
            if Review.objects.filter(
                    author=request.user,
                    title_id=title_id
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв на это произведение.'
                )
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализации вложенных комментариев к отзыву."""
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        exclude = ('review',)

    def validate(self, attrs):
        if self.context['request'].method == 'POST':
            review_id = self.context.get('review_id')
            user = self.context['request'].user
            if Comment.objects.filter(
                    review_id=review_id,
                    author=user
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили комментарий к этому отзыву'
                )
        return attrs


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+\Z',
            message='Недопустимые символы в username!'
        )]
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                "Нельзя использовать 'me' как username!"
            )
        return value

    def validate(self, data):
        existing_user = User.objects.filter(email=data['email']).first()
        if existing_user and existing_user.username != data['username']:
            raise serializers.ValidationError({
                'email': 'Этот email принадлежит другому пользователю'
            })
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    """Сериализатор для получения JWT-токена."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=False,
        default=User.USER
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate_role(self, value):
        if value not in dict(User.ROLE_CHOICES):
            raise serializers.ValidationError("Недопустимая роль")
        return value


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор объектов модели Category."""

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор объектов модели Genre."""

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleGETSerializer(serializers.ModelSerializer):
    """Сериализатор объектов модели Title для GET запросов."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(default=constants.DEFAULT_RATING_VALUE)

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
    """Сериализатор объектов модели Title."""

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
    year = serializers.IntegerField(validators=[validate_year])

    class Meta:
        model = Title
        fields = (
            'name',
            'year',
            'description',
            'genre',
            'category'
        )

    def to_representation(self, title):
        return TitleGETSerializer(title).data
