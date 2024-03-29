from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register', RegisterView.as_view(), name='register'),
    path('games', games, name='games'),
    path('user/<int:user_id>', user, name='userpage'),
    path('usersearch', usersearch, name='usersearch'),
    path('users/', UsersView.as_view(), name='users'),
    path('shop', shop, name='shop'),
    path('item/<int:item_id>', item, name='item'),
    path('buy/<int:item_id>', buy, name='buy'),
    path('nemoney', nemoney, name='nemoney'),
    path('guilds', guilds, name='guilds'),
    path('createguild', createguild, name='createguild'),
    path('guild/<int:guild_id>', guild, name='guild'),
    path('joinguild/<int:guild_id>', joinguild, name='joinguild'),
    path('leaveguild/<int:guild_id>', leaveguild, name='leaveguild'),
    path('promote/<int:guild_id>/<int:user_id>', promote, name='promote'),
    path('demote/<int:guild_id>/<int:user_id>', demote, name='demote'),
    path('forum', forum, name='forum'),
    path('friends', friends, name='friends'),
    path('sendrequest', sendrequest, name='sendrequest'),
    path('acceptrequest/<int:request_id>', acceptrequest, name='acceptrequest'),
    path('declinerequest/<int:request_id>', declinerequest, name='declinerequest'),
    path('messages', messages, name='messages'),
    path('sendmessage', sendmessage, name='sendmessage'),
    path('settings', settings, name='settings'),
    path('applysettings', applysettings, name='applysettings')
]
