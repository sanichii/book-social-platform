from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from .forms import LoginForm, RegisterForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, "Your account has been created successfully!"
            )
            return redirect('accounts:profile')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            messages.success(request, f"Welcome back, {form.user.username}!")
            return redirect('accounts:profile')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('accounts:login')


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    return render(request, 'accounts/profile.html', {'user': request.user})