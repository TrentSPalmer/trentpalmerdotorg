from django.urls import path, reverse_lazy
from django.contrib.auth import views as av
from .enable_totp import enable_totp, disable_totp
from .login import log_in, two_factor_input
from . import views

app_name = "accounts"

urlpatterns = [
    path('login/', log_in, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.log_out, name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('password-change/', views.password_change, name='password_change'),
    path('enable-totp/', enable_totp, name='enable_totp'),
    path('disable-totp/', disable_totp, name='disable_totp'),
    path('two-factor-input/', two_factor_input, name='two_factor_input'),

    path('reset-password/', av.PasswordResetView.as_view(
        template_name='base_form.html',
        email_template_name="accounts/password_reset_email.html",
        success_url=reverse_lazy('accounts:password_reset_done')),
        name='password_reset'),

    path(
        'reset-password-sent/',
        av.PasswordResetDoneView.as_view(template_name='accounts/password_change_done.html'),
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/', av.PasswordResetConfirmView.as_view(
        template_name='accounts/set_password_form.html',
        success_url=reverse_lazy('accounts:password_reset_complete')),
        name="password_reset_confirm"),

    path('reset-password-complete/', av.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'),
        name="password_reset_complete"),
]
