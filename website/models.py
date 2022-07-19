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

class Message(models.Model):
    sender = models.IntegerField()
    sender_name = models.CharField(max_length=150)
    receiver = models.IntegerField()
    receiver_name = models.CharField(max_length=150)
    title = models.CharField(max_length=150)
    content = models.TextField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sender_name = User.objects.get(pk=self.sender).username
        self.receiver_name = User.objects.get(pk=self.receiver).username

    def __str__(self):
        return self.title

class FriendRequest(models.Model):
    sender = models.IntegerField()
    sender_name = models.CharField(max_length=150)
    receiver = models.IntegerField()
    receiver_name = models.CharField(max_length=150)

    def __init__(self):
        self.sender_name = User.objects.get(pk=self.sender).username
        self.receiver_name = User.objects.get(pk=self.receiver).username

    def __str__(self):
        return str(self.sender)
