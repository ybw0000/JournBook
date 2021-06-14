import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import SignUpForm
from django.shortcuts import render, redirect


def sign_up_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('registration/new_acc_confirm_template.html', {
                'user':user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to = [to_email])
            email.send()
            messages.add_message(request, messages.SUCCESS, 'Please confirm your email address. Email was sent to your entered email address', extra_tags='signup_confirm')
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', context={'form':form})

def activate(request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None:
            user.is_active = True
            user.save()
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Sign up success', extra_tags='sign_up_success')
            return redirect('/')
        else:
            return HttpResponse('Activation link is invalid!')

def PasswordChangeView(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            password = request.POST['new_password1']
            user.set_password(password)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Password updated successfully', extra_tags='pass_update')
            return redirect('/')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', context={'form':form})

def LoginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Login success', extra_tags='login_success')
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, 'Login or password is not correct', extra_tags='login_error')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', context={'form': form})