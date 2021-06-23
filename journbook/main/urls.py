from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('like/', views.like_post, name='like-post'),
    path('comments/', views.comments, name='comments'),
    path('leave_comment/', views.leave_comment, name='leave-comment'),
]
