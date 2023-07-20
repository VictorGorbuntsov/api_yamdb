from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator)
from .validators import validate_username
from api.constants import (USERNAME_MAX_LENGTH,
                           EMAIL_MAX_LENGTH,
                           CONFIRMATION_CODE_MAX_LENGTH)

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

USER_ROLES = (
    (ADMIN, 'Admin'),
    (MODERATOR, 'Moderator'),
    (USER, 'User'),
)


def get_len_role(users):
    start_len = 0
    for i in users:
        if len(i[0]) > start_len:
            start_len = len(i[0])
    return start_len


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        verbose_name='Имя пользователя',
        validators=[validate_username]
    )

    bio = models.TextField(
        verbose_name='Биография пользователя',
        blank=True
    )
    email = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Адрес электронной почты',
    )
    role = models.CharField(
        max_length=get_len_role(USER_ROLES),
        choices=USER_ROLES,
        default=USER,
        verbose_name='Роль пользователя'
    )
    confirmation_code = models.CharField(
        max_length=CONFIRMATION_CODE_MAX_LENGTH,
        blank=True,
        verbose_name='Код входа'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR


class Category(models.Model):
    name = models.CharField(
        'Категория',
        max_length=200,
        unique=True
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(
        'Жанр',
        max_length=200,
        unique=True
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Наименование и атрибуты произведений."""

    name = models.CharField(max_length=150, unique=True)
    year = models.IntegerField('Дата выпуска')
    rating = models.FloatField(null=True)
    description = models.TextField(max_length=300, blank=True)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

    def __str__(self) -> str:
        return f'{self.name}'


class GenreTitle(models.Model):
    """Связывающая модель для ManyToMany."""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class TextAuthorDateBaseModel(models.Model):
    text = models.TextField(
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        abstract = True

    def str(self):
        return (
            f'{self.author} - {self.pub_date} - {self.text[:100]}'
        )


class Review(TextAuthorDateBaseModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.IntegerField(
        verbose_name='Оценка произведения',
        validators=(MinValueValidator(1), MaxValueValidator(10))
    )

    class Meta(TextAuthorDateBaseModel.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_title_author'
            )
        ]


class Comment(TextAuthorDateBaseModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta(TextAuthorDateBaseModel.Meta):
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
