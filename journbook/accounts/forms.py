from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User, Post


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'biography', 'username', 'email')

class CreatePostForm(forms.Form):
    text = forms.CharField(max_length=100)
    pictures = forms.ImageField()