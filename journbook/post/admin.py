from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post, Like

admin.site.register(Post)
admin.site.register(Like)