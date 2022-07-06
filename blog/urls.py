from django.urls import path

from .views import *

urlpatterns = [
    path('blog/', index, name='index'),
    path('blog/<int:page>', home, name='bloghome')
]
