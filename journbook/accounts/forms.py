from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=32, help_text='Enter email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
