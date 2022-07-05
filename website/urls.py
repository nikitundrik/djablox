from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register', RegisterView.as_view(), name='register'),
    path('games', games, name='games'),
    path('user/<int:user_id>', user, name='userpage')
]
