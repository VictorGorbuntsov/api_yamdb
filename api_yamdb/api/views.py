from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import LimitOffsetPagination

from api.serializers import (CategorySerializer, GenreSerializer, MeSerializer,
                             MyUserSerializer, SignUpSerializer,
                             TitleCreateAndUpdateSerializer, TitleSerializer,
                             TokenSerializer, ReviewCreateSerializer,
                             CommentSerializer, ReviewSerializer)
from reviews.models import Category, Genre, MyUser, Title, Review, Comment

from .permissions import IsAdmin, OnlyRead, IsOwner


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


class CategoryViewSet(viewsets.ModelViewSet):
    """Представление категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return (AllowAny(),)
        return (IsAdmin(),)


class GenreViewSet(viewsets.ModelViewSet):
    """Представление жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return (AllowAny(),)
        return (IsAdmin(),)


class TitleViewSet(viewsets.ModelViewSet):
    """Представление произведений."""

    queryset = Title.objects.all().annotate(Avg('reviews__score')).\
        select_related('category').prefetch_related('genre')
    serializer_class = TitleSerializer
    permission_classes = (OnlyRead, IsAdmin,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('name', 'year', 'category__slug', 'genre__slug',)
    ordering_fields = ['name', 'year']

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleCreateAndUpdateSerializer
        return TitleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        genre_slug = self.request.query_params.get('genre')
        category_slug = self.request.query_params.get('category')
        if genre_slug:
            queryset = queryset.filter(genre__slug=genre_slug)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    """Представление комментов к отзыву."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsOwner,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(title.reviews, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление отзывов."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsOwner,)

    filter_backends = (filters.OrderingFilter,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
