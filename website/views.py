from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

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
    items = user.owns.split(', ')
    items.remove('')
    print(items)
    items1 = list()
    for item in items:
        print(item)
        item_object = Item.objects.get(name__exact=item)
        items1.append(item_object)
    context = {'user1': user, 'items': items1}
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
    guilds = Guild.objects.order_by('-member_amount')[0:10]
    context = {'guilds': guilds}
    return render(request, 'website/guilds.html', context)


def guild(request, guild_id):
    class GuildMember:
        def __init__(self, name, rank, is_owner, is_admin, account):
            self.name = name,
            self.rank = rank,
            self.is_owner = is_owner
            self.is_admin = is_admin
            self.account = account
    guild = Guild.objects.get(pk=guild_id)
    members_names = guild.members.split(', ')[::2]
    try:
        members_names.remove('')
    except Exception:
        pass
    members_ranks = guild.members.split(', ')[1::2]
    print(members_names)
    print(members_ranks)
    members = list()
    is_user_admin = False
    user_joined = False
    for i in range(len(members_names)):
        is_owner = False
        is_admin = False
        new_name = members_names[i].replace('(', '')
        new_rank = members_ranks[i].replace(')', '')
        if new_rank == 'Owner':
            is_owner = True
            if request.user.username == new_name:
                is_user_admin = True
        if new_rank == 'Admin':
            is_admin = True
            if request.user.username == new_name:
                is_user_admin = True
        if new_name == request.user.username:
            user_joined = True
        member = GuildMember(new_name, new_rank, is_owner, is_admin, User.objects.get(username__exact=new_name))
        members.append(member)
    context = {'guild': guild, 'members': members, 'is_user_admin': is_user_admin, 'user_joined': user_joined}
    return render(request, 'website/guild.html', context)


def joinguild(request, guild_id):
    guild = Guild.objects.get(pk=guild_id)
    guild.member_amount += 1
    guild.members += '(' + request.user.username + ', Member), '
    guild.save()
    return redirect('/guild/' + str(guild_id))


def leaveguild(request, guild_id):
    guild = Guild.objects.get(pk=guild_id)
    position = guild.members.find('(' + request.user.username)
    final_pos = None
    is_bracket = False
    for i in range(position, len(guild.members)):
        if guild.members[i] == ')':
            is_bracket = True
        elif guild.members[i] == ',' and is_bracket == True:
            final_pos = i + 1
    substr = guild.members[position:final_pos]
    guild.members = guild.members.replace(substr, '')
    guild.member_amount -= 1
    guild.save()
    return redirect('/guild/' + str(guild_id))


def promote(request, guild_id, user_id):
    pass


def demote(request, guild_id, user_id):
    pass


def createguild(request):
    guild = Guild(name=request.POST['name'], description=request.POST['description'], members='(' + request.user.username + ', Owner), ')
    guild.save()
    if request.user.coin >= 10:
        request.user.coin -= 10
        request.user.save()
        return redirect('/guild/' + str(guild.id))
    else:
        return redirect('/guilds')


def forum(request):
    return render(request, 'website/forum.html')


def friends(request):
    friends_page = int(request.GET.get('friends', 0))
    requests_page = int(request.GET.get('requests', 0))
    friend_names = request.user.friends.split(', ')[10 * friends_page:10 * (friends_page + 1)]
    friend_names.remove('')
    friends = list()
    for friend in friend_names:
        friend1 = User.objects.get(username__exact=friend)
        friends.append(friend1)
    friend_requests = FriendRequest.objects.filter(receiver__exact=request.user.id)[10 * requests_page:10 * (requests_page + 1)]
    is_fpp = False
    is_fnp = False
    is_rpp = False
    is_rnp = False
    fprevious_page = '/friends/?friends=' + str(friends_page - 1) + '&request=' + str(requests_page)
    fnext_page = '/friends/?friends=' + str(friends_page + 1) + '&request=' + str(requests_page)
    rprevious_page = '/friends/?friends=' + str(friends_page) + '&request=' + str(requests_page - 1)
    rnext_page = '/friends/?friends=' + str(friends_page) + '&request=' + str(requests_page + 1)
    context = {'friends': friends, 'requests': friend_requests, 'is_fpp': is_fpp, 'is_fnp': is_fnp, 'is_rpp': is_rpp, 'is_rnp': is_rnp,
    'fprevious_page': fprevious_page, 'fnext_page': fnext_page, 'rprevious_page': rprevious_page, 'rnext_page': rnext_page}
    return render(request, 'website/friends.html', context)


def sendrequest(request):
    receiver = User.objects.get(username__exact=request.POST['user'])
    request = FriendRequest(sender=request.user.id, sender_name=request.user.username, receiver=receiver.id, receiver_name=request.POST['user'])
    request.save()
    return redirect('/friends')


def acceptrequest(request, request_id):
    friend_request = FriendRequest.objects.get(pk=request_id)
    user = User.objects.get(pk=friend_request.sender)
    request.user.friends += user.username + ', '
    user.friends += request.user.username + ', '
    request.user.save()
    user.save()
    friend_request.delete()
    return redirect('/friends')


def declinerequest(request, request_id):
    friend_request = FriendRequest.objects.get(pk=request_id)
    friend_request.delete()
    return redirect('/friends')


def messages(request):
    received_page = int(request.GET.get('received', 0))
    sent_page = int(request.GET.get('sent', 0))
    received = Message.objects.filter(receiver__icontains=request.user.id)[1 * received_page:10 * (received_page + 1)]
    sent = Message.objects.filter(sender__icontains=request.user.id)[1 * sent_page:10 * (sent_page + 1)]
    is_rpp = False
    is_rnp = False
    is_spp = False
    is_snp = False
    rprevious_page = '/messages/?received=' + str(received_page - 1) + '&sent=' + str(sent_page)
    rnext_page = '/messages/?received=' + str(received_page + 1) + '&sent=' + str(sent_page)
    sprevious_page = '/messages/?received=' + str(received_page) + '&sent=' + str(sent_page - 1)
    snext_page = '/messages/?received=' + str(received_page) + '&sent=' + str(sent_page + 1)
    context = {'received': received, 'sent': sent, 'rprevious_page': rprevious_page, 'rnext_page': rnext_page, 'sprevious_page': sprevious_page, 'snext_page': snext_page,
    'is_rpp': is_rpp, 'is_rnp': is_rnp, 'is_spp': is_spp, 'is_snp': is_snp}
    return render(request, 'website/messages.html', context)


def sendmessage(request):
    receiver1 = User.objects.get(username__exact=request.POST['receiver'])
    message = Message(sender=request.user.id, sender_name=request.user.username, receiver=receiver1.id, receiver_name=request.POST['receiver'], title=request.POST['title'], content=request.POST['content'])
    message.save()
    return redirect('/messages')


def settings(request):
    return render(request, 'website/settings.html')


def applysettings(request):
    about_me = request.POST['aboutme']
    request.user.description = about_me
    request.user.save()
    return redirect('user/' + str(request.user.id))
