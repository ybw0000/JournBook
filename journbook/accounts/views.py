from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from accounts.models import User, Post
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect
from accounts.forms import SignUpForm, ProfileEditForm, CreatePostForm


def sign_up_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('new_acc_confirm_template.html', {
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
    return render(request, 'signup.html', context={'form':form})

def activate(request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None:
            user.is_active = True
            user.save()
            # username = user.username
            # password = user.password
            # user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Sign up success', extra_tags='sign_up_success')
            return redirect('profile_edit')
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
    return render(request, 'password_change.html', context={'form':form})

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
    return render(request, 'login.html', context={'form': form})

def ProfileEditView(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        user = request.user
        user.first_name = form['first_name'].value()
        user.last_name = form['last_name'].value()
        user.biography = form['biography'].value()
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Profile info updated successfully')
        return redirect('index')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'profile_edit.html', context={'form':form})

def ProfileView(request, id):
    if request.method == 'POST':
        user = User.objects.filter(pk = id)
        return redirect(request, 'profile.html', locals())
    else:
        user = User.objects.filter(pk = id)
    return render(request, 'profile.html', locals())

# def CreatePostView(request):
#     if request.method == 'POST':
#         # form = CreatePostForm(request.POST)
#         # if form.is_valid():
#             print('-' * 100)
#             print(request.FILES)
#             print(request.POST)
#             post_new = Post.objects.create(
#                 author=request.user,
#                 text=request.POST['text'],
#                 pictures=request.POST['pictures']
#             )
#             print(request.FILES)
#             print(request.POST)
#             print('-' * 100)
#             post_new.save()
#             messages.add_message(request, messages.SUCCESS, 'Post added successfully')
#             return redirect('index')
#         # else:
#         #     messages.add_message(request, messages.ERROR, 'Form is not valid')
#         #     return render(request, 'create_post.html', context={'form':form})
#     else:
#         form = CreatePostForm()
#     return render(request, 'create_post.html', context={'form': form})

def CreatePostView(request):
    if request.method == 'POST':
        # form = CreatePostForm(request.POST, request.FILES)
        # if form.is_valid():
            instance = Post(pictures=request.FILES['pictures'], author=request.user, text=request.POST['text'])
            instance.save()
            return redirect('index')
        # else:
        #     messages.add_message(request, messages.ERROR, 'Form is not valid')
        #     return render(request, 'create_post.html', context={'form':form})
    # else:
        # form = CreatePostForm()
    return render(request, 'create_post.html')
