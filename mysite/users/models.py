from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True
    )
    username = models.CharField(
        verbose_name="User name", max_length=100
    )
    phone = models.CharField(
        verbose_name="Office phone",
        max_length=50,
        validators=[
            RegexValidator(
                regex=r"^\+\d{3}[\s\S]*\d{2}[\s\S]*\d{3}[\s\S]*\d{2}[\s\S]*\d{2}$",
                message="Phone number must be in the format: '+999999999999'.",
            )
        ],
    )

    def __str__(self):
        return self.username
