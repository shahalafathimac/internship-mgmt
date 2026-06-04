from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    internship_title = serializers.CharField(
        source="internship.title",
        read_only=True
    )

    class Meta:
        model = Application
        fields = [
            "id",
            "student",
            "internship",
            "internship_title",
            "applied_at"
        ]

        read_only_fields = [
            "student",
            "applied_at"
        ]