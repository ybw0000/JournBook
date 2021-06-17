from django.shortcuts import render
from django.conf import settings
from accounts.models import User
from post.models import Post

def index(request):
    if request.method == 'POST':
        return render(request, 'main/index.html')
    else:
        return render(request, 'main/index.html')

def index(request):
    posts = Post.objects.all()
    return render(request, 'main/index.html', {'posts':posts})
