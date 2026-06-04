from django.shortcuts import render
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Application
from .serializers import ApplicationSerializer
from apps.internships.models import Internship



class ApplyInternshipAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, internship_id):
        if request.user.role != "student":
            return Response(
                {
                    "message": "Only students can apply"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            internship = Internship.objects.get(
                id=internship_id
            )
        except Internship.DoesNotExist:
            return Response(
                {
                    "message": "Internship not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            application = Application.objects.create(
                student=request.user,
                internship=internship
            )

        except IntegrityError:
            return Response(
                {
                    "message": "You have already applied for this internship"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ApplicationSerializer(
            application
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class MyApplicationsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        applications = Application.objects.filter(
            student=request.user
        )
        serializer = ApplicationSerializer(
            applications,
            many=True
        )
        return Response(serializer.data)