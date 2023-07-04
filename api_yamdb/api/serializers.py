from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from reviews.models import MyUser


class MyUserSerializer(serializers.ModelSerializer):
    """Сериализатор для Юзера"""
    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class SignUpSerializer(serializers.Serializer):
    """Сериализатор отправки письма"""
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)

    def validate(self, data):
        if data['username'].lower() == 'me':
            raise ValidationError('Нельзя использовать слово "me" в имени')
        return data

    class Meta:
        model = MyUser
        fields = ('username', 'email')


class TokenSerializer(serializers.Serializer):
    """Cериализатор получения токена"""
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = MyUser
        fields = ('username', 'confirmation_code')


class MeSerializer(serializers.ModelSerializer):
    """Сериализатор для эндпоинта users/me"""
    role = serializers.CharField(read_only=True)

    class Meta:
        model = MyUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
