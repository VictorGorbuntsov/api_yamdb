from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from reviews.models import Category, Genre, MyUser, Title, Comment, Review
from reviews.validators import validate_year


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания отзывов."""
    author = serializers.SlugRelatedField(
        slug_field="user_name",
        read_only=True,
    )
    score = serializers.IntegerField(min_value=0, max_value=10)

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = get_object_or_404(
            id=self.context['request'].parser_context['kwargs']['title_id']
        )
        if Review.objects.filter(
            author=self.context['request'].user,
            title=title
        ).exists():
            raise serializers.ValidationError('Отзыв уже оставлен')
        return data

    class Meta:
        fields = '__all__'
        model = Review
        read_only = 'id'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с комментариями."""
    review = serializers.SlugRelatedField(
        slug_field="text",
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        slug_field="user_name",
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only = 'id'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с отзывами."""
    author = serializers.SlugRelatedField(
        slug_field="user_name",
        read_only=True,
    )
    score = serializers.IntegerField(min_value=0, max_value=10)

    class Meta:
        fields = '__all__'
        model = Review
        read_only = 'id'


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
    """Cериализатор получения токена"""
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
