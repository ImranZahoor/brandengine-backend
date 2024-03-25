from allauth.account.forms import SignupForm, ResetPasswordForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from allauth.account.adapter import get_adapter
from allauth.account.utils import (
    filter_users_by_email,
    user_pk_to_url_str,
    user_username,
)
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from allauth.account.forms import default_token_generator
from django.urls import reverse
from dj_rest_auth.app_settings import api_settings
from allauth.utils import build_absolute_uri
from allauth.account import app_settings as allauth_account_settings

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """


class UserResetPasswordForm(ResetPasswordForm):
    def clean_email(self):
        """
        Invalid email should not raise error, as this would leak users
        for unit test: test_password_reset_with_invalid_email
        """
        email = self.cleaned_data["email"]
        email = get_adapter().clean_email(email)
        self.users = filter_users_by_email(email, is_active=True)
        return self.cleaned_data["email"]

    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data["email"]
        token_generator = kwargs.get("token_generator", default_token_generator)

        for user in self.users:
            temp_key = token_generator.make_token(user)

            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()

            # send the password reset email
            path = reverse(
                "password_reset_confirm",
                args=[user_pk_to_url_str(user), temp_key],
            )

            if api_settings.PASSWORD_RESET_USE_SITES_DOMAIN:
                url = build_absolute_uri(None, path)
            else:
                url = build_absolute_uri(request, path)

            url = url.replace("%3F", "?")
            url = (
                settings.RESET_PASSWORD_URL
                + path.split("/")[-2]
                + "/"
                + path.split("/")[-1]
            )
            context = {
                "current_site": current_site,
                "user": user,
                "password_reset_url": url,
                "request": request,
                "message": "",
                "action": "Reset",
                "support_message": "Please click the link below to reset your password. "
                "If you've not requested a password reset, "
                "feel free to ignore this email and continue with your previous password.",
            }
            if (
                allauth_account_settings.AUTHENTICATION_METHOD
                != allauth_account_settings.AuthenticationMethod.EMAIL
            ):
                context["username"] = user_username(user)
            get_adapter(request).send_mail(
                "account/email/password_reset_key", email, context
            )
        return self.cleaned_data["email"]
