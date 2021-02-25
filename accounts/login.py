from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import EnableTotpForm
from django.contrib.auth import login
from .models import Account
from django.contrib.auth.models import User
from django.contrib import messages
import pyotp
from time import sleep


def log_in(request):
    if request.user.is_authenticated:
        return redirect('audio:home')
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not hasattr(user, 'account'):
                account = Account(user=user)
                account.save()
                user.account = account
            if user.account.use_totp:
                request.session['user_id'] = user.id
                request.session['totp_timeout'] = 1
                return redirect('accounts:two_factor_input')
            else:
                login(request, user)
                messages.success(request, 'Successfully logged in!', extra_tags="mb-0")
                return redirect('audio:home')
    else:
        form = AuthenticationForm()
    return render(request, 'base_form.html', {'form': form})


def two_factor_input(request):
    if request.user.is_authenticated:
        return redirect('audio:home')
    if 'user_id' not in request.session:
        return redirect('audio:home')
    user = User.objects.get(id=request.session['user_id'])
    if request.method == "POST":
        form = EnableTotpForm(request.POST, instance=user.account)
        if form.is_valid():
            totp_code = form.cleaned_data['totp_code']
            if pyotp.TOTP(user.account.totp_key).verify(int(totp_code), valid_window=5):
                login(request, user)
                del request.session['user_id']
                messages.success(request, 'Successfully logged in!', extra_tags="mb-0")
                return redirect('audio:home')
            else:
                form = EnableTotpForm(instance=user.account)
                messages.error(request, 'Wrong Code, try again?', extra_tags="mb-0")
                sleep(request.session['totp_timeout'])
                request.session['totp_timeout'] = request.session['totp_timeout'] * 2
    else:
        form = EnableTotpForm(instance=user.account)
    return render(request, 'accounts/totp_form.html', {'form': form})
