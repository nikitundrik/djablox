from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    description = models.TextField(blank=True)
    owns = models.TextField(blank=True)
    coin = models.IntegerField(default=0)
    materia = models.IntegerField(default=0)

    def __str__(self):
        return self.username

class Item(models.Model):
    name = models.CharField(max_length=20)
    image = models.CharField(max_length=100)
    description = models.TextField()
    price = models.CharField(max_length=100)

    def __str__(self):
        return self.name
