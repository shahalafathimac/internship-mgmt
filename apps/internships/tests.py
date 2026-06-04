from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Internship


class InternshipsAPITests(APITestCase):
    def setUp(self):
        self.company = get_user_model().objects.create_user(
            email="company@example.com",
            password="StrongPass123",
            role="company",
        )
        self.other_company = get_user_model().objects.create_user(
            email="other-company@example.com",
            password="StrongPass123",
            role="company",
        )
        self.student = get_user_model().objects.create_user(
            email="student@example.com",
            password="StrongPass123",
            role="student",
        )
        self.payload = {
            "title": "Backend Intern",
            "description": "Work with Django APIs",
            "stipend": "15000.00",
            "duration": "3 months",
            "location": "Remote",
        }

    def test_internship_create_list_detail_update_and_delete_apis_work(self):
        self.client.force_authenticate(user=self.company)

        create_response = self.client.post(
            "/internships/create/",
            self.payload,
            format="json",
        )

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_response.data["title"], self.payload["title"])
        internship_id = create_response.data["id"]

        self.client.force_authenticate(user=None)
        list_response = self.client.get("/internships/")
        detail_response = self.client.get(f"/internships/{internship_id}/")

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data["id"], internship_id)

        self.client.force_authenticate(user=self.company)
        update_response = self.client.put(
            f"/internships/update/{internship_id}/",
            {
                **self.payload,
                "title": "Updated Backend Intern",
            },
            format="json",
        )

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data["title"], "Updated Backend Intern")

        delete_response = self.client.delete(f"/internships/delete/{internship_id}/")

        self.assertEqual(delete_response.status_code, status.HTTP_200_OK)
        self.assertFalse(Internship.objects.filter(id=internship_id).exists())

    def test_only_company_can_create_internship(self):
        self.client.force_authenticate(user=self.student)

        response = self.client.post(
            "/internships/create/",
            self.payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_only_owner_company_can_update_or_delete_internship(self):
        internship = Internship.objects.create(
            company=self.company,
            **self.payload,
        )
        self.client.force_authenticate(user=self.other_company)

        update_response = self.client.put(
            f"/internships/update/{internship.id}/",
            {
                **self.payload,
                "title": "Not Allowed",
            },
            format="json",
        )
        delete_response = self.client.delete(f"/internships/delete/{internship.id}/")

        self.assertEqual(update_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_missing_internship_detail_returns_not_found(self):
        response = self.client.get("/internships/999/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
