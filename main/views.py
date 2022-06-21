from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from main.models import PhotoGraphy, Category
from django.contrib import messages
from main.forms import LoginForm, RegistrationForm, ChangePasswordForm
from django.contrib.auth import get_user_model

User = get_user_model()


def index(request, *args, **kwargs):
    return render(request, 'main/index.html')


# def about_profile_view(request, username, *args, **kwargs):
#     user = User.objects.get(username=username)
#     projects = user.project.all()
#     context = {
#         'user': user,
#         'projects': projects
#     }
#     return render(request, 'main/about.html', context)


def about_profile_view(request, username, *args, **kwargs):
    user = User.objects.get(username=username)

    context = {
        'user': user,
    }
    return render(request, 'main/about.html', context)


def registration_view(request, *args, **kwargs):
    form = RegistrationForm()

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data.get('first_name')
            lastname = form.cleaned_data.get('last_name')

            user = form.save()
            message = f"{firstname} {lastname} has been created"
            messages.success(request, message)
            return redirect('login')
        else:
            message = f'Error processing form'
            messages.error(request, message)


def login_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email_or_username = form.cleaned_data.get('email_or_username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email_or_username, password=password)
            login(request, user)
            messages.success(request, 'Successfully Logged In')
            return redirect('home')
    context = {
        'form': form
    }
    template_name = 'accounts/login.html'
    return render(request, template_name, context)


def logout_view(request, *args, **kwargs):
    logout(request)
    message = 'You have successfully logged out'
    messages.success(request, message)
    return redirect('login-view')


def password_update(request, *args, **kwargs):
    form = ChangePasswordForm(user=request.user)
    if request.method == "POST":
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            print(form.user)
            update_session_auth_hash(request, user=form.user)
            return redirect('profile')
        else:
            message = 'Error in processing form'
            messages.error(request, message)
    context = {}
    template = 'accounts/password_update.html'
    return render(request, template, context)
