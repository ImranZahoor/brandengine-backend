from django.db import models
from utils.model_utils import Timestamp
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class DraftProfile(Timestamp):
    title = models.CharField(max_length=255, blank=False, null=False)
    category = models.CharField(max_length=255, blank=False, null=False)
    query = models.CharField(max_length=255, blank=False, null=False)
    brand_name = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(null=True, blank=True)
    logo = models.CharField(max_length=255, blank=True, null=True, default=None)
    description = models.TextField(null=True, blank=True)
    insta = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    insta_followers = models.IntegerField(null=True, blank=True)
    facebook_followers = models.IntegerField(null=True, blank=True)
    result_number = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Draft Profiles"

    def __str__(self):
        return self.title
