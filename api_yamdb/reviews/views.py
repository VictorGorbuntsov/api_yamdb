<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
from reviews.models import MyUser
from api.serializers import (SignUpSerializer, TokenSerializer,
                             MyUserSerializer, MeSerializer)
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets


class MyUserViewSet(viewsets.ModelViewSet):
    """Вьюсет для Юзера"""
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    filter_backends = (filters.SearchFilter,)
    search_field = 'username'
    lookup_field = 'username'

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
    )
    def me(self, request):
        """Функция для эндпоинта 'users/me"""
        user = get_object_or_404(MyUser, username=self.request.user)
        if request.method == 'GET':
            serializer = MeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = MeSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    """Функция для запроса кода доступа"""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    user, create = MyUser.objects.get_or_create(
        username=username,
        email=email
    )
    code = default_token_generator.make_token(user)
    user.confirmation_code = code
    user.save()
    send_mail(
        'Регистрация',
        f'Ваш код для регистрации: {code}',
        from_email='admin@yamdb.com',
        # recipient_list=('soita.pavel@yandex.ru',),
        recipient_list=(email,),
        fail_silently=False
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Функция для получения токена"""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(MyUser, username=username)
    if default_token_generator.check_token(user, code):
        token = str(AccessToken.for_user(user))
        return Response({'token': token}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
>>>>>>> a2f300a (qwqw)
