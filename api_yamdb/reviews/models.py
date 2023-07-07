from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator

from .validators import validate_year

USER_ROLES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class MyUser(AbstractUser):
    username = models.CharField(
        max_length=154,
        unique=True,
        verbose_name='Имя пользователя'
    )
    bio = models.TextField(
        verbose_name='Биография пользователя',
        blank=True
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты',
    )
    role = models.CharField(
        max_length=20,
        choices=USER_ROLES,
        default='user',
        verbose_name='Роль пользователя'
    )
    confirmation_code = models.CharField(
        max_length=32,
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
        if self.role == 'admin':
            return True
        else:
            return False


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

    name = models.CharField(max_length=256, blank=False)
    year = models.IntegerField(validators=[validate_year])
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


class Review(models.Model):
    title = models.ForeignKey(
        Title,  # произведение
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Название',
    )
    author = models.ForeignKey(
        MyUser,
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
        MyUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
