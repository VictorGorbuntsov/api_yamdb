from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Genre, MyUser, Title
from reviews.validators import validate_year


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
        fields = fields = (
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
