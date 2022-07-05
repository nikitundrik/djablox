from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register', RegisterView.as_view(), name='register')
]
