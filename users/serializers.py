from dj_rest_auth.registration.serializers import RegisterSerializer
from django.conf import settings
from django.core.validators import RegexValidator
import django.db.models
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from allauth.account import app_settings as allauth_account_settings
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.account.utils import setup_user_email
from django.contrib.auth import get_user_model, authenticate
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from django.urls import exceptions as url_exceptions

User = get_user_model()


def email_address_exists(email, exclude_user=None):
    from allauth.account import app_settings as account_settings
    from allauth.account.models import EmailAddress

    emailaddresses = EmailAddress.objects
    if exclude_user:
        emailaddresses = emailaddresses.exclude(user=exclude_user)
    ret = emailaddresses.filter(email__iexact=email).exists()
    if not ret:
        email_field = account_settings.USER_MODEL_EMAIL_FIELD
        if email_field:
            users = get_user_model().objects
            if exclude_user:
                users = users.exclude(pk=exclude_user.pk)
            ret = users.filter(**{email_field + "__iexact": email}).exists()
    return ret


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone = serializers.CharField(validators=[phone_regex])
    email = serializers.EmailField(required=allauth_account_settings.EMAIL_REQUIRED)
    is_brand = serializers.BooleanField(default=False)

    def validate(self, data):
        errors = {}

        email = get_adapter().clean_email(data["email"])
        if allauth_account_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                errors["email"] = [
                    "A user is already registered with this email address."
                ]
                errors["verified"] = [EmailAddress.objects.get(email=email).verified]

        if data["password1"] != data["password2"]:
            errors["password"] = ["The two password fields didn't match."]

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict["first_name"] = self.validated_data.get("first_name", "")
        data_dict["phone"] = self.validated_data.get("phone", "")
        data_dict["email"] = self.validated_data.get("email").lower()
        data_dict["is_brand"] = self.validated_data.get("is_brand")
        data_dict["last_name"]=self.validated_data.get("last_name", "")

        return data_dict

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()

        user.is_brand = self.cleaned_data.get("is_brand", False)
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name =self.validated_data.get("last_name", "")
        user.phone = self.cleaned_data.get("phone", "")
        user.email = self.cleaned_data.get("email").lower()

        user = adapter.save_user(request, user, self, commit=False)
        user.last_login = None
        user.save()

        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        
        return user


    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_email, user_field

        data = form.cleaned_data
        name = data.get("name")
        email = data.get("email").lower()
        user_email(user, email)
        if name:
            user_field(user, "name", name)
        else:
            user.set_unusable_password()
        # self.populate_username(request, user)
        if commit:
            user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={"input_type": "password"})

    def authenticate(self, **kwargs):
        return authenticate(self.context["request"], **kwargs)

    def _validate_email(self, email, password):
        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username(self, username, password):
        if username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username_email(self, username, email, password):
        if email and password:
            user = self.authenticate(email=email, password=password)
        elif username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include either "username" or "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def get_auth_user_using_allauth(self, username, email, password):
        from allauth.account import app_settings as allauth_account_settings

        # Authentication through email
        if (
            allauth_account_settings.AUTHENTICATION_METHOD
            == allauth_account_settings.AuthenticationMethod.EMAIL
        ):
            return self._validate_email(email, password)

        # Authentication through username
        if (
            allauth_account_settings.AUTHENTICATION_METHOD
            == allauth_account_settings.AuthenticationMethod.USERNAME
        ):
            return self._validate_username(username, password)

        # Authentication through either username or email
        return self._validate_username_email(username, email, password)

    def get_auth_user_using_orm(self, username, email, password):
        if email:
            try:
                username = User.objects.get(email__iexact=email).get_username()
            except User.DoesNotExist:
                pass

        if username:
            return self._validate_username_email(username, "", password)

        return None

    def get_auth_user(self, username, email, password):
        """
        Retrieve the auth user from given POST payload by using
        either `allauth` auth scheme or bare Django auth scheme.

        Returns the authenticated user instance if credentials are correct,
        else `None` will be returned
        """
        if "allauth" in settings.INSTALLED_APPS:
            # When `is_active` of a user is set to False, allauth tries to return template html
            # which does not exist. This is the solution for it. See issue #264.
            try:
                return self.get_auth_user_using_allauth(username, email, password)
            except url_exceptions.NoReverseMatch:
                msg = _("Unable to log in with provided credentials.")
                raise exceptions.ValidationError(msg)
        return self.get_auth_user_using_orm(username, email, password)

    @staticmethod
    def validate_auth_user_status(user):
        if not user.is_active:
            msg = _("User account is disabled.")
            raise exceptions.ValidationError(msg)

    @staticmethod
    def validate_email_verification_status(user):
        from allauth.account import app_settings as allauth_account_settings

        if (
            allauth_account_settings.EMAIL_VERIFICATION
            == allauth_account_settings.EmailVerificationMethod.MANDATORY
            and not user.emailaddress_set.filter(
                email=user.email, verified=True
            ).exists()
        ):
            raise serializers.ValidationError({"verified": ["False"]})

    def validate(self, attrs):
        username = attrs.get("username")

        email = attrs.get("email").lower()
        password = attrs.get("password")
        user = self.get_auth_user(username, email, password)

        if email_address_exists(email):
            current_user = User.objects.get(email=email)
            verified = EmailAddress.objects.get(email=current_user.email).verified
            if not verified and not user:
                msg = _(
                    "Your email address has not been verified yet. "
                    "Kindly check your email to set password."
                )
                raise exceptions.ValidationError(msg)

        if not user:
            msg = _("Invalid email or password.")
            raise exceptions.ValidationError(msg)

        if user:
            user_auth = EmailAddress.objects.get(email=user.email)
            user_auth.verified = True
            user_auth.save()

        # Did we get back an active user?
        self.validate_auth_user_status(user)

        # If required, is the email verified?
        if "dj_rest_auth.registration" in settings.INSTALLED_APPS:
            self.validate_email_verification_status(user)

        attrs["user"] = user

        return attrs


class UserSerializer(serializers.ModelSerializer):
    profile_picture = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "profile_picture",
            "dob",
            "is_brand",
        ]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }