from django.urls import path, include
from rest_framework import routers
from .views import MyUserViewSet, sign_up, get_token

router = routers.DefaultRouter()

router.register('users', MyUserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', sign_up, name='sign_up'),
    path('v1/auth/token/', get_token, name='get_token')
]
