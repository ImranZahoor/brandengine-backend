from django.contrib.auth import get_user_model
from django.db import models
from utils.model_utils import Timestamp
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class BrandUser(Timestamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='brand_user')
    type = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _("brand user")
        verbose_name_plural = _("Brand Users")
