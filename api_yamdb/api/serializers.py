from rest_framework import serializers
from rest_framework.exceptions import ValidationError
# from rest_framework.generics import get_object_or_404
from reviews.models import Category, Genre, Title, Comment, Review, CustomUser
from reviews.validators import validate_year, validate_username
from reviews.models import Category, Genre, Title, Comment, Review, CustomUser
from reviews.models import Category, Comment, Genre, CustomUser, Review, Title
from reviews.validators import validate_year
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (ModelSerializer,
                                        SlugRelatedField, IntegerField)
from django.core.validators import (MaxValueValidator, MinValueValidator)
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
# from django.contrib.auth.tokens import default_token_generator
from api.constants import (USERNAME_MAX_LENGTH, EMAIL_MAX_LENGTH,
                           ERROR_REVIEW_AUTHOR_UNIQUE)

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
        if (self.context.get('request').method == 'POST'
                and Review.objects.filter(
                    author=self.context.get('request').user,
                    title=self.context.get('view').kwargs.get('title_id'))
                .exists()):
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


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для Юзера"""
    username = serializers.CharField(
        required=True,
        max_length=USERNAME_MAX_LENGTH,
        validators=[validate_username,
                    UniqueValidator(queryset=CustomUser.objects.all())]
    )

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

        validators = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
                fields=('username', 'email'))
        ]


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'confirmation_code')
        extra_kwargs = {
            'username': {'validators': []},
            'email': {'validators': []}
        }


class SignUpSerializer(serializers.Serializer):
    """Сериализатор отправки письма."""

    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH, required=True)
    username = serializers.CharField(
        required=True,
        max_length=USERNAME_MAX_LENGTH,
        validators=[validate_username]
    )

    # def create(self, validated_data):
    #     """Создание токена"""
    #     user = super().create(validated_data)
    #     user.confirmation_code = default_token_generator.make_token(user)
    #     user.save()
    #     return user

    # def validate(self, data):
    #     """Проверка уникальности Username и Email"""
    #     if CustomUser.objects.filter(username=data.get('username')):
    #         raise serializers.ValidationError(
    #             'Пользователь с таким именем уже существует'
    #         )
    #     if CustomUser.objects.filter(email=data.get('email')):
    #         raise serializers.ValidationError(
    #             'Пользователь с таким email уже существует'
    #         )
    #     return data


class TokenSerializer(serializers.Serializer):
    """Cериализатор получения токена"""
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[validate_username]
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code',)


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
    rating = serializers.IntegerField(read_only=True)

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

    def create(self, validated_data):
        title = super().create(validated_data)
        return title

    def update(self, instance, validated_data):
        title = super().update(instance, validated_data)
        return title

    def validate_genre(self, value):
        if not value:
            raise serializers.ValidationError(
                "Список жанров не может быть пустым.")
        return value
