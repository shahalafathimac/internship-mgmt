from django.urls import path
from .views import (
    ApplyInternshipAPIView,
    MyApplicationsAPIView
)

urlpatterns = [
    path('apply/<int:internship_id>/',ApplyInternshipAPIView.as_view(),name='apply-internship'),
    path('my-applications/',MyApplicationsAPIView.as_view(),name='my-applications'),
]