from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_post_view, name='create_post')
]
