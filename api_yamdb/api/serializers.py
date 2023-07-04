from rest_framework import serializers
from User.models import Comment, Review
from rest_framework.generics import get_object_or_404


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
