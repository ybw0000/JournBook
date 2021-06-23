from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.sign_up_view, name='signup'),
    path('password_change/', views.password_change_view, name='password_change'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('profile/<id>/', views.profile_view, name='profile'),
    path('profile/<id>/follow', views.follow, name='follow')
]
