from django.db import models


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
        User,
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
