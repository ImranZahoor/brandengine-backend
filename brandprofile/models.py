from django.db import models
from utils.model_utils import Timestamp
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class BrandProfile(Timestamp):
    name = models.CharField(max_length=255, blank=False, null=False)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="brand_category"
    )
    search_tags = models.TextField(null=True, blank=True)
    website = models.URLField()
    logo = models.ImageField(upload_to="logo/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    insta = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message=_(
            "Phone number must be entered in the format: '+999999999'. "
            "Up to 15 digits allowed."
        ),
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    email = models.EmailField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner_brand"
    )

    class Meta:
        verbose_name_plural = "Brand Profiles"

    def __str__(self):
        return self.name


class BrandLocation(models.Model):
    brand = models.ForeignKey(BrandProfile, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Brand Locations"

    def __str__(self):
        return f"{self.id} - {self.country}"
