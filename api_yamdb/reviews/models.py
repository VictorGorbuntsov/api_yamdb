from django.contrib.auth.models import AbstractUser
from django.db import models

USER_ROLES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class MyUser(AbstractUser):
    # username = models.CharField(
    #     max_length=154,
    #     unique=True,
    #     verbose_name='Имя пользователя'
    # )
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


class Title(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        'Автор',
        MyUser,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='posts',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Genre(models.Model):
    name = models.CharField(
        'Жанр',
        max_length=200,
        unique=True
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.slug
