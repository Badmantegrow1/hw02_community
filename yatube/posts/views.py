from django.shortcuts import render, get_object_or_404
from .models import Post, Group


def index(request):
    posts = Post.objects.all()[:10]
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)


def group_post(request, slug):
    NUMBER_OF_POSTS = 10
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).all()[:NUMBER_OF_POSTS]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)
