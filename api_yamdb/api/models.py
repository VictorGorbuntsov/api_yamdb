from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import MaxValueValidator

User = get_user_model()


class Title(models.Model):
    ...


class Review(models.Model):
    title = models.ForeignKey(
        Title,  # произведение
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст')
    score = models.PositiveIntegerField(
        validators=[MaxValueValidator(10,)]
    )
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Ревью'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
