from api.constants import (EMAIL_MAX_LENGTH, ERROR_REVIEW_AUTHOR_UNIQUE,
                           USERNAME_MAX_LENGTH)
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        SlugRelatedField)
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from reviews.models import Category, Comment, CustomUser, Genre, Review, Title
from reviews.validators import validate_username, validate_year


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


class SignUpSerializer(serializers.Serializer):
    """Сериализатор отправки письма."""

    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH, required=True)
    username = serializers.CharField(
        required=True,
        max_length=USERNAME_MAX_LENGTH,
        validators=[validate_username]
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def create(self, validated_data):
        """Создание кода доступа"""
        user, created = CustomUser.objects.get_or_create(**validated_data)
        if created:
            user.save()
            return user
        else:
            return validated_data

    def validate(self, data):
        """Проверка уникальности Username и Email"""

        if not CustomUser.objects.filter(
            username=data.get("username"), email=data.get("email")
        ).exists():
            if CustomUser.objects.filter(username=data.get("username")):
                raise serializers.ValidationError(
                    "Пользователь с таким именем уже существует"
                )
            if CustomUser.objects.filter(email=data.get("email")):
                raise serializers.ValidationError(
                    "Пользователь с таким еmail уже существует"
                )

        return data


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

    def to_representation(self, value):
        if isinstance(value, Title):
            serializer = TitleSerializer(value)
        else:
            raise Exception('Что-то пошло не так.')
        return serializer.data

    def validate_genre(self, value):
        if not value:
            raise serializers.ValidationError(
                "Список жанров не может быть пустым.")
        return value
