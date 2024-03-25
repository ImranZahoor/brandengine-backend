from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.model_utils import Timestamp
from django.urls import reverse


class User(AbstractUser, Timestamp):
    email = models.EmailField(unique=True)
    is_brand = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    dob = models.DateField(null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message=_(
            "Phone number must be entered in the format: '+999999999'. "
            "Up to 15 digits allowed."
        ),
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    profile_picture = models.ImageField(
        _("Profile picture of User"),
        blank=True,
        null=True,
        upload_to="profile_pictures",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("Users")

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
