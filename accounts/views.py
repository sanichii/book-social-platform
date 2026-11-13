
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import (
    LoginForm,
    ProfileUpdateForm,
    RegisterForm,
    UserUpdateForm,
)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('posts:feed')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                "Your account has been created successfully!"
            )
            return redirect('posts:feed')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard:index')
        return redirect('posts:feed')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            messages.success(
                request,
                f"Welcome back, {form.user.username}!"
            )

            if form.user.is_staff:
                return redirect('dashboard:index')

            return redirect('posts:feed')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('accounts:login')


@login_required(login_url='accounts:login')
def profile_view(request):
    return render(
        request,
        'accounts/profile.html',
        {'user': request.user}
    )


@login_required(login_url='accounts:login')
def profile_edit_view(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request,
                "Your profile has been updated successfully!"
            )
            return redirect('accounts:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(
            instance=request.user.profile
        )

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(
        request,
        'accounts/profile_edit.html',
        context
    )
