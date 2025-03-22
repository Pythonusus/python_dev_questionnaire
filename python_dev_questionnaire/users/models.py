from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # We use the default user model by django.contrib.auth.
    # Only email field is redefined to be required and unique.
    email = models.EmailField(
        verbose_name="Email",
        blank=False,
        null=False,
        unique=True,
    )
