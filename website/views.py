from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .models import *

def home(request):
    return render(request, 'website/home.html')


class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'website/register.html'


def games(request):
    return render(request, 'website/games.html')


def user(request, user_id):
    user = User.objects.get(pk=user_id)
    context = {'user': user}
    return render(request, 'website/user.html', context)
