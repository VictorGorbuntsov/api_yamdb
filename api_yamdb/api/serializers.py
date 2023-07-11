from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from reviews.models import Category, Genre, Title, Comment, Review, MyUser
from reviews.validators import validate_year
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (ModelSerializer,
                                        SlugRelatedField, IntegerField)
from django.core.validators import (MaxValueValidator, MinValueValidator)

ERROR_REVIEW_AUTHOR_UNIQUE = (
    'Нельзя оставлять несколько отзывов на одно произведение'
)


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    score = IntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(10))
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)

    def validate(self, data):
        if self.context.get('request').method != 'POST':
            return data
        reviewer = self.context.get('request').user
        if get_object_or_404(
                Title, id=self.context.get('view').kwargs.get('title_id')
        ).reviews.filter(author=reviewer):
            raise ValidationError(ERROR_REVIEW_AUTHOR_UNIQUE)
        return data


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)


class MyUserSerializer(serializers.ModelSerializer):
    """Сериализатор для Юзера."""
    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class SignUpSerializer(serializers.Serializer):
    """Сериализатор отправки письма."""
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)

    def validate(self, data):
        if data['username'].lower() == 'me':
            raise ValidationError('Нельзя использовать слово "me" в имени')
        return data

    class Meta:
        model = MyUser
        fields = ('username', 'email',)


class TokenSerializer(serializers.Serializer):
    """Cериализатор получения токена."""
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = MyUser
        fields = ('username', 'confirmation_code',)


class MeSerializer(serializers.ModelSerializer):
    """Сериализатор для эндпоинта users/me."""
    role = serializers.CharField(read_only=True)

    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""

    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )

    class Meta:
        model = Title
        fields = '__all__'


class TitleCreateAndUpdateSerializer(serializers.ModelSerializer):
    """Сериадлизатор для создания и обновления названия произведения."""

    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    year = serializers.IntegerField(validators=[validate_year])

    class Meta:
        model = Title
        fields = '__all__'
