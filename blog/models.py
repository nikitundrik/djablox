from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=20)
    date = models.DateField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return self.title
