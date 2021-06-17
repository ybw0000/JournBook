from django.shortcuts import render, redirect
from django.conf import settings
from accounts.models import User
from post.models import Post, Like

def index(request):
    if request.method == 'POST':
        return render(request, 'main/index.html')
    else:
        return render(request, 'main/index.html')

def index(request):
    posts = Post.objects.all()
    user = request.user
    return render(request, 'main/index.html', {
        'posts':posts,
        'user':user,
    })

def like_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST['post_id']
        post_obj = Post.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = Like.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

        like.save()
    return redirect('index')