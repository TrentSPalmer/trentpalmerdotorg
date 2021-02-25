from django.shortcuts import redirect, render
import qrcode.image.svg
from .forms import EnableTotpForm
from django.contrib import messages
from .models import Account
from io import BytesIO
import pyotp
import qrcode


def disable_totp(request):
    if not request.user.is_authenticated:
        return redirect('audio:home')
    if not request.user.account.use_totp:
        return redirect('audio:home')
    if request.method == "POST":
        account = Account.objects.get(user=request.user)
        account.use_totp = False
        account.totp_key = None
        account.save()
        messages.success(request, 'Thanks for disabling 2fa!', extra_tags="mb-0")
        return(redirect('accounts:edit_profile'))
    return render(request, 'confirmation.html', {})


def enable_totp(request):
    if not request.user.is_authenticated:
        return redirect('audio:home')
    qr = get_totp_qr(request.user)
    if request.method == "POST":
        form = EnableTotpForm(request.POST, instance=request.user.account)
        if form.is_valid():
            totp_code = form.cleaned_data['totp_code']
            if pyotp.TOTP(request.user.account.totp_key).verify(int(totp_code), valid_window=5):
                account = Account.objects.get(user=request.user)
                account.use_totp = True
                account.save()
                messages.success(request, 'Thanks for enabling 2fa!', extra_tags="mb-0")
                return(redirect('accounts:edit_profile'))
            else:
                messages.error(request, 'Wrong Code, try again?', extra_tags="mb-0")
    else:
        form = EnableTotpForm(instance=request.user.account)
    return render(request, 'accounts/totp_form.html', {'form': form, 'qr': qr})


def get_totp_qr(user):
    if user.account.totp_key is None:
        account = Account.objects.get(user=user)
        account.totp_key = pyotp.random_base32()
        account.save()
        user.account.totp_key = account.totp_key

    totp_uri = pyotp.totp.TOTP(user.account.totp_key).provisioning_uri(name='audio', issuer_name='trentpalmer.org')
    img = qrcode.make(totp_uri, image_factory=qrcode.image.svg.SvgPathImage)
    f = BytesIO()
    img.save(f)
    return(f.getvalue().decode('utf-8'))
