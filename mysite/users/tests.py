from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from users.models import Profile


class Base(APITestCase):
    def setUp(self) -> None:
        self.user_one = User.objects.create_user(
            username='testuser1',
            password='testpassword'
        )
        self.user_two = User.objects.create_user(
            username='testuser2',
            password='testpassword'
        )

class UserRegistrationAPIView(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse("registration-list")

    def test_post(self):
        response = self.client.post(self.url, data=dict(
            username="TestUser",
            email="testuser@example.com",
            password="Password123",
        ))
        answer = {"message": f"New User was created"}
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, answer)
        user_exist = User.objects.get(id=1)
        self.assertTrue(user_exist)
        profile_exist = Profile.objects.get(id=1)
        self.assertTrue(profile_exist)
