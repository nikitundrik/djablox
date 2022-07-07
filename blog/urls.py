from django.urls import path

from .views import *

urlpatterns = [
    path('blog/', index, name='index'),
    path('blog/<int:page>', home, name='bloghome'),
    path('blog/posts/<int:post_id>', post, name='post')
]
