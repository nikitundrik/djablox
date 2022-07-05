from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    description = models.TextField(blank=True)
    owns = models.TextField(blank=True)

    def __str__(self):
        return self.username
