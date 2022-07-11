from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q

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


def usersearch(request):
    return render(request, 'website/usersearch.html')


class UsersView(generic.ListView):
    model = User
    template_name = 'website/user_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_name = self.request.GET.get('q', '')
        page = int(self.request.GET.get('page', 0))
        is_pp = False
        is_np = False
        previous_page = '/users/?q=' + user_name + '&page=' + str(page - 1)
        next_page = '/users/?q=' + user_name + '&page=' + str(page + 1)
        if page != 0:
            is_pp = True
        if len(User.objects.filter(username__icontains=user_name)) > 10 * (page + 1):
            is_np = True
        context['users'] = User.objects.filter(username__icontains=user_name)[1 * page:10 * (page + 1)]
        context['is_pp'] = is_pp
        context['is_np'] = is_np
        context['previous_page'] = previous_page
        context['next_page'] = next_page
        return context



def shop(request):
    items = Item.objects.order_by('id')[0:10]
    context = {'items': items}
    return render(request, 'website/shop.html', context)


def guilds(request):
    return render(request, 'website/guilds.html')


def forum(request):
    return render(request, 'website/forum.html')
