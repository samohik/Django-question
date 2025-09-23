import datetime

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

from answers.models import Answer
from question.models import Question
from users.models import Profile


class Base(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.time = datetime.datetime.now().strftime("%Y-%m-%d")


        # First user
        self.user_one = User.objects.create_user(
            username='testuser1',
            password='testpassword'
        )
        self.profile_one = Profile.objects.create(
            user=self.user_one,
            username='testuser1',
        )

        self.question_from_user_one = Question.objects.create(
            created_by=self.profile_one,
            text="Text for test from user 1",
        )

        # Second user
        self.user_two = User.objects.create_user(
            username='testuser2',
            password='testpassword'
        )
        self.profile_two= Profile.objects.create(
            user=self.user_two,
            username='testuser2',
        )

        self.question_from_user_two = Question.objects.create(
            created_by=self.profile_two,
            text="Text for test from user 2",
        )

        #   Answer from user 2 to user 1

        self.answer_from_user_two_to_user_one = Answer.objects.create(
            question_id=self.question_from_user_one,
            user_id=self.profile_two,
            text="Test",
        )


class QuestionsAPIView(Base):
    def test_get(self):
        self.url = reverse("questions-list")
        with self.assertNumQueries(1):
            response = self.client.get(self.url)

            answer = [
                {
                    'created_by': 'testuser1',
                    'text': 'Text for test from user 1',
                    'created_at': self.time,
                },
                {
                    'created_by': 'testuser2',
                    'text': 'Text for test from user 2',
                    'created_at': self.time,
                }
            ]
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, answer)

    def test_get_id(self):
        url = reverse("questions-detail", kwargs={"pk": 1})
        with self.assertNumQueries(2):

            response = self.client.get(url)
            answer = {
                'created_by': 1,
                'text': 'Text for test from user 1',
                'created_at': self.time,
                'question_answer': [
                    {
                        'question_id': 1,
                        'user_id': 2,
                        'text': 'Test',
                        'created_at': self.time,
                    }
                ]
            }
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, answer)

    def test_post(self):
        self.client.force_authenticate(user=self.user_one)

        self.url = reverse("questions-list")
        text = "Test for post from user One"
        response = self.client.post(
            self.url,
            data={"text": text},
        )

        answer = {"message": "Created"}
        question_from_user_one = Question.objects.get(id=3)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(question_from_user_one.text, text)
        self.assertEqual(question_from_user_one.created_by, self.profile_one)
        self.assertEqual(response.data, answer)

    def test_delete_successful(self):
        self.client.force_authenticate(user=self.user_one)
        url = reverse("questions-detail", kwargs={"pk": 1})
        response = self.client.delete(url)

        # Checking deletion Question
        question = Question.objects.filter(id=1).first()
        self.assertFalse(question)

        # Checking deletion Answers
        answer = Answer.objects.filter(id=1).first()
        self.assertFalse(answer)

        self.assertEqual(response.status_code, 204)

    def test_delete_failed(self):
        self.client.force_authenticate(user=self.user_two)
        url = reverse("questions-detail", kwargs={"pk": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)