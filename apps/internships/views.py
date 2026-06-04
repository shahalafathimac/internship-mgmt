from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Internship
from .serializers import InternshipSerializer

class InternshipCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'company':
            return Response(
                {
                    "message": "Only companies can create internships"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = InternshipSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save(
                company=request.user
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



class InternshipListAPIView(APIView):
    def get(self, request):
        internships = Internship.objects.all()
        serializer = InternshipSerializer(
            internships,
            many=True
        )
        return Response(serializer.data)


class InternshipDetailAPIView(APIView):

    def get(self, request, pk):
        try:
            internship = Internship.objects.get(
                pk=pk
            )
        except Internship.DoesNotExist:
            return Response(
                {
                    "message": "Internship not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = InternshipSerializer(
            internship
        )
        return Response(serializer.data)


class InternshipUpdateAPIView(APIView):

    permission_classes = [IsAuthenticated]
    def put(self, request, pk):

        try:
            internship = Internship.objects.get(
                pk=pk
            )
        except Internship.DoesNotExist:
            return Response(
                {
                    "message": "Internship not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if internship.company != request.user:
            return Response(
                {
                    "message": "Permission denied"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = InternshipSerializer(
            internship,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class InternshipDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        try:
            internship = Internship.objects.get(
                pk=pk
            )
        except Internship.DoesNotExist:
            return Response(
                {
                    "message": "Internship not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if internship.company != request.user:
            return Response(
                {
                    "message": "Permission denied"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        internship.delete()
        return Response(
            {
                "message": "Internship deleted successfully"
            }
        )