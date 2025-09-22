from django.db import models

from question.models import Question
from users.models import Profile


class Answer(models.Model):
    question_id = models.ForeignKey(
        Question,
        verbose_name="Question ID",
        on_delete=models.CASCADE,
        related_name="question_answer",
        blank=True,
        null=True,
    )
    user_id = models.ForeignKey(
        Profile,
        verbose_name="User ID",
        on_delete=models.CASCADE,
        related_name="user_answer",
        blank=True,
        null=True,
    )
    text = models.TextField(
        verbose_name="Text",
    )
    created_at = models.DateTimeField(
        verbose_name="Creation date",
        auto_now_add=True,
    )


    def __str__(self):
        return f"{self.id}"
