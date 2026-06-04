from django.db import models
from apps.accounts.models import User


class Internship(models.Model):
    company = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='internships'
    )
    title = models.CharField(
        max_length=255
    )
    description = models.TextField()
    stipend = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    duration = models.CharField(
        max_length=100
    )
    location = models.CharField(
        max_length=255
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title
