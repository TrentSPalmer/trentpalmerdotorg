from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from .forms import OurUserCreationForm
from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from .forms import EditProfileForm


def password_change(request):
    if not request.user.is_authenticated:
        return redirect('audio:home')
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!', extra_tags="mb-0")
            return redirect('accounts:edit_profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'base_form.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('audio:home')
    if request.method == "POST":
        form = OurUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Registered!', extra_tags="mb-0")
            return redirect('accounts:login')
    else:
        form = OurUserCreationForm()
    return render(request, 'base_form.html', {'form': form})


def log_out(request):
    if not request.user.is_authenticated:
        return redirect('audio:home')
    if request.method == "POST":
        logout(request)
        messages.success(request, 'Successfully Logged Out!', extra_tags="mb-0")
        return redirect('audio:home')
    return render(request, 'confirmation.html', {})


def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('audio:home')
    if request.method == "POST":
        form = EditProfileForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!', extra_tags="mb-0")
            return redirect('audio:home')
    else:
        form = EditProfileForm(request.user, initial={
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        })
    return render(request, 'base_form.html', {'form': form})
