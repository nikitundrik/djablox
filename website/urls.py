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
    path('forum', forum, name='forum'),
    path('messages', messages, name='messages'),
    path('sendmessage', sendmessage, name='sendmessage'),
    path('settings', settings, name='settings'),
    path('applysettings', applysettings, name='applysettings')
]
