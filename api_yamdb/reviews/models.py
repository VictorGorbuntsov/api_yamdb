from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import (MaxValueValidator,
                                    RegexValidator,
                                    MinValueValidator)
from reviews.validators import validate_year

USER_ROLES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class MyUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя',
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя содержит недопустимый символ'
        )]
    )

    bio = models.TextField(
        verbose_name='Биография пользователя',
        blank=True
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Адрес электронной почты',
    )
    role = models.CharField(
        max_length=20,
        choices=USER_ROLES,
        default='user',
        verbose_name='Роль пользователя'
    )
    confirmation_code = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Код входа'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        if self.role == 'user':
            return True
        else:
            return False

    @property
    def is_moderator(self):
        if self.role == 'moderator':
            return True
        else:
            return False

    @property
    def is_admin(self):
        if self.role == 'admin' or self.is_superuser:
            return True
        else:
            return False


class BaseCategory(models.Model):
    name = models.CharField(
        'Название',
        max_length=256,
        unique=True
    )
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        abstract = True
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(BaseCategory):
    class Meta(BaseCategory.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseCategory):
    class Meta(BaseCategory.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Наименование и атрибуты произведений."""

    name = models.CharField(max_length=256, blank=False)
    year = models.FloatField(validators=[validate_year], db_index=True)
    description = models.TextField('Описание')
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
        MyUser,
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
