from django.urls import path
from .views import (
    InternshipCreateAPIView,
    InternshipListAPIView,
    InternshipDetailAPIView,
    InternshipUpdateAPIView,
    InternshipDeleteAPIView,
)

urlpatterns = [

    path('create/',InternshipCreateAPIView.as_view()),
    path('',InternshipListAPIView.as_view()),
    path('<int:pk>/',InternshipDetailAPIView.as_view()),
    path('update/<int:pk>/',InternshipUpdateAPIView.as_view()),
    path('delete/<int:pk>/',InternshipDeleteAPIView.as_view()),
]