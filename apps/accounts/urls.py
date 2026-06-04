from django.urls import path
from .views import (
    RegisterAPIView,
    ProfileAPIView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/',RegisterAPIView.as_view(),name='register'),
    path('login/',TokenObtainPairView.as_view(),name='login'),
    path('refresh/',TokenRefreshView.as_view(),name='refresh'),
    path('profile/',ProfileAPIView.as_view(),name='profile'),
]