from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from reviews.models import Category, Genre, Title, Comment, Review
from reviews.validators import validate_year


class RewiewCreatSerializers(serializers.ModelSerializer):
    """Сериадлизатор для создания отзывов."""
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
        read_only = ('id')


class RewiewSerializers(serializers.ModelSerializer):
    """Сериализатор для работы с отзывами."""
    author = serializers.SlugRelatedField(
        slug_field="user_name",
        read_only=True,
    )
    score = serializers.IntegerField(min_value=0, max_value=10)

    class Meta:
        fields = '__all__'
        model = Review
        read_only = ('id')


class CommentSerializers(serializers.ModelSerializer):
    """Сериалихатор для работы с комментариями."""
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
        read_only = ('id')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=True)
    category = CategorySerializer()

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
