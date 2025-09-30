import datetime

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
        url = reverse("questions-list")
        with self.assertNumQueries(2):
            response = self.client.get(url)
            answer = [
                {
                    "id": 1,
                    'created_by': self.profile_one.username,
                    'text': 'Text for test from user 1',
                    'created_at': self.time,
                },
                {
                    "id": 2,
                    'created_by': self.profile_two.username,
                    'text': 'Text for test from user 2',
                    'created_at': self.time,
                }

            ]
            # [{
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, answer)

    def test_get_detail(self):
        url = reverse("questions-detail", kwargs={"pk": 1})
        with self.assertNumQueries(2):

            response = self.client.get(url)
            answer = {
                "id": 1,
                'created_by': self.profile_one.id,
                'text': 'Text for test from user 1',
                'created_at': self.time,
                'answer_questions': [
                    {
                        "id": 1,
                        'question_id': self.question_from_user_one.id,
                        'user_id': self.profile_two.id,
                        'text': 'Test',
                        'created_at': self.time,
                    }
                ]
            }

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, answer)

    def test_post(self):
        self.client.force_authenticate(user=self.user_one)

        url = reverse("questions-list")
        text = "Test for post from user One"
        response = self.client.post(
            url,
            data={
                "text": text,
            },
        )

        answer = {
            "id": 3,
            "text": "Test for post from user One",
            "created_by": self.profile_one.username,
            "created_at": self.time,
        }
        question_from_user_one = Question.objects.get(id=3)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(question_from_user_one.text, text)
        self.assertEqual(question_from_user_one.created_by, self.profile_one)
        self.assertEqual(response.data, answer)

    def test_post_detail(self):
        self.client.force_authenticate(user=self.user_two)
        url = reverse("questions-answers", kwargs={"pk": 1})
        response = self.client.post(
            url,
            data={
                "text": "Text for post Detail",
            }
        )
        result = {
            "id": 2,
            "question_id": self.question_from_user_one.id,
            "user_id": self.profile_two.id,
            "text": "Text for post Detail",
            "created_at": self.time,
        }
        self.assertEqual(response.data, result)
        self.assertEqual(response.status_code, 201)


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