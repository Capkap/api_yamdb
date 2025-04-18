from rest_framework import serializers
from reviews.models import Review, Comment
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    pub_date = serializers.DateTimeField(read_only=True)
    score = serializers.IntegerField(
        validators=[
            serializers.MinValueValidator(1),
            serializers.MaxValueValidator(10)
        ],
        error_messages={'validators': 'Оценка должна быть от 1 до 10'}
    )
    title = serializers.IntegerField(source='title.id')

    def validate(self, attrs):
        # Проверка на уникальность отзыва
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
    author = serializers.CharField(source='author.username', read_only=True)
    review = serializers.IntegerField(source='review.id')

    class Meta:
        model = Comment
        fields = ('id', 'review', 'text', 'author')