from django.shortcuts import render
from django.conf import settings
from accounts.models import User, Post

def index(request):
    if request.method == 'POST':
        return render(request, 'main/index.html')
    else:
        return render(request, 'main/index.html')

def index(request):

    posts = Post.objects.all()
    context={'posts':posts, 'media_url':settings.MEDIA_URL}
    return render(request, 'main/index.html', context)
