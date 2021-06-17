from django.shortcuts import render, redirect
from django.conf import settings
from accounts.models import User
from post.models import Post, Like, Comment
from post.forms import CommentForm

def index(request):
    if request.method == 'POST':
        return render(request, 'main/index.html')
    else:
        return render(request, 'main/index.html')

def index(request):
    posts = Post.objects.all()
    comments = Comment.objects.all()
    all_data = []
    for post in posts:
        all_data.append(
            {
                'text': post.text,
                'author':post.author,
                'picture':post.picture,
                'pub_date':post.pub_date,
                'id':post.id,
                'liked':post.liked,
                'comments':Comment.objects.filter(post_id = post.id).order_by('-id')[:2][::-1]
            }
        )

    user = request.user
    return render(request, 'main/index.html', {
        'posts':all_data,
        'user':user,
        'comments':comments,
    })

def like_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST['post_id']
        post_obj = Post.objects.get(id = post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = Like.objects.get_or_create(
            user = user,
            post_id = post_id
        )

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

        like.save()
    return redirect('index')

def leave_comment(request):

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            user = request.user
            post_id = request.POST['post_id']

            comment = Comment.objects.create(
                user = user,
                post_id = post_id,
                comment_text= request.POST['comment_text']
            )

            comment.save()
    return redirect('index')
