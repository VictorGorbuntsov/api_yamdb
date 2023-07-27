from api.serializers import (CategorySerializer, CommentSerializer,
                             CustomUserSerializer, GenreSerializer,
                             ReviewSerializer, SignUpSerializer,
                             TitleCreateAndUpdateSerializer, TitleSerializer,
                             TokenSerializer)
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, CustomUser, Genre, Review, Title

from api_yamdb.settings import ADMIN_EMAIL

from .filters import TitleFilter
from .mixins import ListDestroyCreateWithFilters
from .permissions import IsAdmin, IsOwner, OnlyRead


class CategoryViewSet(ListDestroyCreateWithFilters):
    """Представление категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListDestroyCreateWithFilters):
    """Представление жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Представление произведений."""

    queryset = Title.objects.all().annotate(rating=Avg(
        'reviews__score'
    )).select_related('category').prefetch_related('genre')
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    permission_classes = (OnlyRead | IsAdmin,)
    filterset_fields = ('name', 'year', 'category__slug', 'genre__slug',)
    ordering_fields = ('name', 'year')
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleCreateAndUpdateSerializer
        return TitleSerializer


class ReviewViewSet(ModelViewSet):
    """Представление отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwner,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwner,)

    def get_review_object(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review_object().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        review=get_object_or_404(Review,
                                                 id=self.kwargs['review_id']))


class CustomUserViewSet(viewsets.ModelViewSet):
    """Вьюсет для Юзера"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        """Функция для эндпоинта 'users/me"""
        user = get_object_or_404(CustomUser, username=request.user.username)
        if request.method == 'GET':
            serializer = CustomUserSerializer(user)
        if request.method == 'PATCH':
            serializer = CustomUserSerializer(user,
                                              data=request.data,
                                              partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=self.request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def sign_up(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(CustomUser, username=request.data.get('username'))
    code = default_token_generator.make_token(user)
    user.confirmation_code = code
    user.save()
    send_mail(
        'Регистрация',
        f'Ваш код для регистрации: {code}',
        from_email=ADMIN_EMAIL,
        recipient_list=(user.email,),
        fail_silently=False
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
# @permission_classes([AllowAny])
def get_token(request):
    """Функция для получения токена"""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(CustomUser, username=username)
    if default_token_generator.check_token(user, code):
        token = str(AccessToken.for_user(user))
        return Response({'token': token}, status=status.HTTP_201_CREATED)
    return Response('Введен некорректный код доступа',
                    status=status.HTTP_400_BAD_REQUEST)
