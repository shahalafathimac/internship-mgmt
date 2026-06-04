from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


class AccountsAPITests(APITestCase):
    def test_register_login_refresh_and_profile_apis_work(self):
        register_response = self.client.post(
            "/accounts/register/",
            {
                "email": "student@example.com",
                "password": "StrongPass123",
                "role": "student",
                "phone": "9876543210",
            },
            format="json",
        )

        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(register_response.data["data"]["email"], "student@example.com")

        login_response = self.client.post(
            "/accounts/login/",
            {
                "email": "student@example.com",
                "password": "StrongPass123",
            },
            format="json",
        )

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)
        self.assertIn("refresh", login_response.data)

        refresh_response = self.client.post(
            "/accounts/refresh/",
            {
                "refresh": login_response.data["refresh"],
            },
            format="json",
        )

        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", refresh_response.data)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {login_response.data['access']}"
        )
        profile_response = self.client.get("/accounts/profile/")

        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data["email"], "student@example.com")

    def test_profile_requires_authentication(self):
        response = self.client.get("/accounts/profile/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_duplicate_email_registration_fails(self):
        get_user_model().objects.create_user(
            email="student@example.com",
            password="StrongPass123",
            role="student",
        )

        response = self.client.post(
            "/accounts/register/",
            {
                "email": "student@example.com",
                "password": "StrongPass123",
                "role": "student",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
