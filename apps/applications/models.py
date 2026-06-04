from django.db import models
from django.db.models import UniqueConstraint
from apps.accounts.models import User
from apps.internships.models import Internship


class Application(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    internship = models.ForeignKey(
        Internship,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["student", "internship"],
                name="unique_student_internship"
            )

        ]

    def __str__(self):
        return f"{self.student.username} - {self.internship.title}"
