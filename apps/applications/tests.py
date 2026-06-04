from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.internships.models import Internship

from .models import Application


class ApplicationsAPITests(APITestCase):
    def setUp(self):
        self.company = get_user_model().objects.create_user(
            email="company@example.com",
            password="StrongPass123",
            role="company",
        )
        self.student = get_user_model().objects.create_user(
            email="student@example.com",
            password="StrongPass123",
            role="student",
        )
        self.internship = Internship.objects.create(
            company=self.company,
            title="Backend Intern",
            description="Work with Django APIs",
            stipend="15000.00",
            duration="3 months",
            location="Remote",
        )

    def test_apply_and_my_applications_apis_work(self):
        self.client.force_authenticate(user=self.student)

        apply_response = self.client.post(
            f"/applications/apply/{self.internship.id}/",
            {},
            format="json",
        )

        self.assertEqual(apply_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(apply_response.data["internship"], self.internship.id)
        self.assertEqual(apply_response.data["internship_title"], self.internship.title)

        my_applications_response = self.client.get("/applications/my-applications/")

        self.assertEqual(
            my_applications_response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(my_applications_response.data), 1)
        self.assertEqual(
            my_applications_response.data[0]["internship"],
            self.internship.id,
        )

    def test_duplicate_application_is_rejected(self):
        Application.objects.create(
            student=self.student,
            internship=self.internship,
        )
        self.client.force_authenticate(user=self.student)

        response = self.client.post(
            f"/applications/apply/{self.internship.id}/",
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_only_students_can_apply(self):
        self.client.force_authenticate(user=self.company)

        response = self.client.post(
            f"/applications/apply/{self.internship.id}/",
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_missing_internship_apply_returns_not_found(self):
        self.client.force_authenticate(user=self.student)

        response = self.client.post("/applications/apply/999/", {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_application_string_uses_student_email(self):
        application = Application.objects.create(
            student=self.student,
            internship=self.internship,
        )

        self.assertEqual(
            str(application),
            "student@example.com - Backend Intern",
        )
