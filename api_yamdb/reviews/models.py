from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from api_yamdb.settings import USER
from titles.models import Title


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Объект отзыва'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Основной текст отзыва',
        blank=False,
        null=False
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        help_text='Оценка от 1 до 10'
    )
    author = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        editable=False
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'Отзыв {self.id} от {self.author.username}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.author = kwargs.pop('author', None)
        super().save(*args, **kwargs)

    @property
    def author_username(self):
        return self.author.username


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Основной текст комментария',
        blank=False,
        null=False
    )
    author = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        editable=False
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:50]
