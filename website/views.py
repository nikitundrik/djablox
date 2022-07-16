from django.contrib.auth.forms import UserCreationForm
from django.dispatch import receiver
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q

from .models import *
from .forms import *

def home(request):
    return render(request, 'website/home.html')


class RegisterView(generic.CreateView):
    form_class = UserCreationForm1
    success_url = reverse_lazy('login')
    template_name = 'website/register.html'


def games(request):
    return render(request, 'website/games.html')


def user(request, user_id):
    user = User.objects.get(pk=user_id)
    context = {'user1': user}
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
    page = int(request.GET.get('page', 0))
    is_pp = False
    is_np = False
    previous_page = '/shop?page=' + str(page - 1)
    next_page = '/shop?page=' + str(page + 1)
    items = Item.objects.order_by('id')[1 * page:10 * (page + 1)]
    if page != 0:
        is_pp = True
    if len(Item.objects.order_by('id')) > 10 * (page + 1):
        is_np = True
    context = {'items': items, 'is_pp': is_pp, 'is_np': is_np, 'previous_page': previous_page, 'next_page': next_page}
    return render(request, 'website/shop.html', context)


def item(request, item_id):
    item = Item.objects.get(pk=item_id)
    context = {'item': item}
    return render(request, 'website/item.html', context)


def buy(request, item_id):
    item = Item.objects.get(pk=item_id)
    price = item.price.split(' ')
    coin_price = int(price[0])
    materia_price = None
    if len(price) > 2:
        materia_price = int(price[2])
    user_coins = request.user.coin
    user_materia = request.user.materia
    if materia_price is None:
        if user_coins > coin_price:
            request.user.coin -= coin_price
            request.user.owns += item.name + ', '
            request.user.save()
            return redirect('/user/' + str(request.user.id))
        else:
            return redirect('/nemoney')
    else:
        if user_coins > coin_price and user_materia > materia_price:
            request.user.coin -= coin_price
            request.user.materia -= materia_price
            request.user.owns += item.name + ', '
            request.user.save()
            return redirect('/user/' + str(request.user.id))
        else:
            return redirect('/nemoney')


def nemoney(request):
    return render(request, 'website/nemoney.html')


def guilds(request):
    return render(request, 'website/guilds.html')


def forum(request):
    return render(request, 'website/forum.html')


def messages(request):
    return render(request, 'website/messages.html')


def sendmessage(request):
    message = Message(sender=request.user.username, receiver=request.POST['receiver'], title=request.POST['title'], content=request.POST['content'])
    message.save()
    return redirect('/messages')


def settings(request):
    return render(request, 'website/settings.html')


def applysettings(request):
    about_me = request.POST['aboutme']
    request.user.description = about_me
    request.user.save()
    return redirect('user/' + str(request.user.id))
