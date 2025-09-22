from django.db import models

from users.models import Profile


class Question(models.Model):
    created_by = models.ForeignKey(
        Profile,
        verbose_name="Created by",
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name="Text for question",
    )
    created_at = models.DateTimeField(
        verbose_name="Creation date",
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.id}"

