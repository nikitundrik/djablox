from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import *

class UserCreationForm1(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")

class UserChangeForm1(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email")