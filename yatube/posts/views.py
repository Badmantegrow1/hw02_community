from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import Post, Group, User


NUMBER_OF_POSTS: int = 10


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_post(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts_group.all()
    paginator = Paginator(post_list, NUMBER_OF_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-pub_date')
    paginator = Paginator(posts, NUMBER_OF_POSTS)
    count = paginator.count
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'user': user,
        'page_obj': page_obj,
        'count': count,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    count = Post.objects.filter(author=post.author).count()
    context = {
        'post': post,
        'count': count,
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            author = User.objects.get(pk=request.user.id)
            post = Post(text=form.cleaned_data['text'], author=author,
                        group=form.cleaned_data['group'])
            post.save()
            return redirect("posts:profile", author.username)
    else:
        form = PostForm()
        context = {'form': form}
        return render(request, 'posts/post_create.html', context)
