from allauth.account.utils import user_pk_to_url_str
from dj_rest_auth.app_settings import api_settings
from django.contrib.sites.shortcuts import get_current_site
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.urls import reverse
from allauth.utils import (
    build_absolute_uri,
    get_user_model,
)
from django.conf import settings
from allauth.account.adapter import get_adapter
from allauth.account.forms import default_token_generator

User = get_user_model()


@receiver(user_signed_up)
def send_password_reset_email(sender, request, user, **kwargs):
    # Send password reset email to the user
    current_site = get_current_site(request)
    temp_key = default_token_generator.make_token(user)
    # default_token_generator.check_token(user, temp_key)
    path = reverse(
        "password_reset_confirm",
        args=[user_pk_to_url_str(user), temp_key],
    )
    if api_settings.PASSWORD_RESET_USE_SITES_DOMAIN:
        url = build_absolute_uri(None, path)
    else:
        url = build_absolute_uri(request, path)
    url = url.replace("%3F", "?")

    url = settings.RESET_PASSWORD_URL + path.split("/")[-2] + "/" + path.split("/")[-1]
    context = {
        "current_site": current_site,
        "user": user,
        "password_reset_url": url,
        "request": request,
        "message": "Welcome to Brand",
        "action": "Set",
        "support_message": "Please click the link below to set your password. If you've not requested a password Set, "
        "feel free to ignore this email.",
    }
    get_adapter(request).send_mail(
        "account/email/password_reset_key", user.email, context
    )
