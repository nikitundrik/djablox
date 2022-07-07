from django.shortcuts import get_object_or_404, redirect, render

from .models import *


def index(request):
    return redirect('/blog/0')


def home(request, page):
    posts = Post.objects.order_by('id')[10 * page:10 * (page + 1)]
    is_pp = False
    is_np = False
    previous_page = page - 1
    next_page = page + 1
    if len(Post.objects.order_by('id')) > 10 * (page + 1):
        is_np = True
    if page != 0:
        is_pp = True
    content = {'posts': posts, 'is_pp': is_pp, 'is_np': is_np, 'previous_page': previous_page, 'next_page': next_page}
    return render(request, 'blog/home.html', content)


def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    paragraphs = post.text.split('(endp)')
    context = {'post': post, 'paragraphs': paragraphs}
    return render(request, 'blog/post.html', context)