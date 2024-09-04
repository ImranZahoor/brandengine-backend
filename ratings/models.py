from django.db import models
from django.contrib.auth import get_user_model
from brandprofile.models import BrandProfile
from utils.model_utils import Timestamp
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Ratings(Timestamp):
    description = models.TextField(null=True, blank=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    proof_of_order = models.ImageField(upload_to="proofs/", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_rating")
    brand_profile = models.ForeignKey(
        BrandProfile, on_delete=models.CASCADE, related_name="brandprofile_rating"
    )
    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"

    def __str__(self):
        return str(self.rating)
