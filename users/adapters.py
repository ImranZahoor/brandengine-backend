import warnings
from typing import Any
from django.shortcuts import resolve_url

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.template.loader import render_to_string

from django.contrib.auth import (
    get_backends,
)
from django.template import TemplateDoesNotExist
from django.core.mail import EmailMessage, EmailMultiAlternatives

from brandusers.models import BrandUser


# from students.models import Student


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.full_name = data.get("full_name")
        user.save()
        if user.is_brand:
            BrandUser.objects.create(user=user)
        return user

    def login(self, request, user):
        # HACK: This is not nice. The proper Django way is to use an
        # authentication backend
        if not hasattr(user, "backend"):
            from allauth.account.auth_backends import AuthenticationBackend

            backends = get_backends()
            backend = None
            for b in backends:
                if isinstance(b, AuthenticationBackend):
                    # prefer our own backend
                    backend = b
                    break
                elif not backend and hasattr(b, "get_user"):
                    # Pick the first valid one
                    backend = b
            backend_path = ".".join([backend.__module__, backend.__class__.__name__])
            user.backend = backend_path
        # django_login(request, user)

    def render_mail(self, template_prefix, email, context, headers=None):
        """
        Renders an e-mail to `email`.  `template_prefix` identifies the
        e-mail that is to be sent, e.g. "account/email/email_confirmation"
        """
        to = [email] if isinstance(email, str) else email
        subject = render_to_string("{0}_subject.txt".format(template_prefix), context)
        # remove superfluous line breaks
        subject = " ".join(subject.splitlines()).strip()
        subject = self.format_email_subject(subject)
        try:
            if context["action"] == "Set":
                subject = "Welcome to Brand"
            elif context["action"] == "Reset":
                subject = "Reset your Password"
        except:
            pass
        from_email = self.get_from_email()

        bodies = {}
        for ext in ["html", "txt"]:
            try:
                template_name = "{0}_message.{1}".format(template_prefix, ext)
                bodies[ext] = render_to_string(
                    template_name,
                    context,
                    self.request,
                ).strip()
            except TemplateDoesNotExist:
                if ext == "txt" and not bodies:
                    # We need at least one body
                    raise
        if "txt" in bodies:
            msg = EmailMultiAlternatives(
                subject, bodies["txt"], from_email, to, headers=headers
            )
            if "html" in bodies:
                msg.attach_alternative(bodies["html"], "text/html")
        else:
            msg = EmailMessage(subject, bodies["html"], from_email, to, headers=headers)
            msg.content_subtype = "html"  # Main content is now text/html
        return msg

    def get_login_redirect_url(self, request):
        """
        Returns the default URL to redirect to after logging in.  Note
        that URLs passed explicitly (e.g. by passing along a `next`
        GET parameter) take precedence over the value returned here.
        """
        assert request.user.is_authenticated
        url = getattr(settings, "LOGIN_REDIRECT_URLNAME", None)
        if url:
            warnings.warn(
                "LOGIN_REDIRECT_URLNAME is deprecated, simply"
                " use LOGIN_REDIRECT_URL with a URL name",
                DeprecationWarning,
            )
        else:
            url = settings.LOGIN_REDIRECT_URL
        print(url)
        return resolve_url(url)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom social account adapter extending DefaultSocialAccountAdapter from Django allauth.
    """

    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        """
        Method to determine if the social signup process is open.

        Args:
        - request (HttpRequest): The HTTP request object.
        - sociallogin (Any): Social login information.

        Returns:
        - bool: True if social signup is allowed, False otherwise.
        """
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


def generate_username(first_name, last_name):
    """
    Function to generate a unique username based on first name and last name.

    Args:
    - first_name (str): User's first name.
    - last_name (str): User's last name.

    Returns:
    - str: A unique username based on provided names.
    """
    val = "{0}{1}".format(first_name, last_name).lower()
    x = 0
    while True:
        if x == 0 and User.objects.filter(username=val).count() == 0:
            return val
        else:
            new_val = "{0}{1}".format(val, x)
            if User.objects.filter(username=new_val).count() == 0:
                return new_val
        x += User.objects.filter(username__contains=val).count() + 1
        if x > 1000000:
            raise Exception("Name is super popular!")
