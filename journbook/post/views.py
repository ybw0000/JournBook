from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import CreatePostForm


def create_post_view(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.add_message(request, messages.SUCCESS, 'Post created successfully')
            return redirect('index')
        else:
            messages.add_message(request, messages.ERROR, 'Form is not valid')
    else:
        form = CreatePostForm()
    return render(request, 'create_post.html', {'form': form})
