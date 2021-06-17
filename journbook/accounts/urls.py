from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.LoginView, name = 'login'),
    path('signup/', views.sign_up_view, name = 'signup'),
    path('password_change/', views.PasswordChangeView, name = 'password_change'),
    path('activate/<uidb64>/<token>', views.activate, name = 'activate'),
    path('profile/edit/', views.ProfileEditView, name = 'profile_edit'),
    path('profile/<id>', views.ProfileView, name = 'profile'),
]