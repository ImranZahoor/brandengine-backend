from django.db import models

from brandprofile.models import BrandProfile
from utils.model_utils import Timestamp


class FollowerTrack(Timestamp):
    brand_profile = models.ForeignKey(
        BrandProfile, on_delete=models.CASCADE, related_name="profile_follower_track"
    )
    insta_count = models.IntegerField()
    fb_count = models.IntegerField()

    class Meta:
        verbose_name = "Follower Track"
        verbose_name_plural = "Followers Track"

    def __str__(self):
        return f"{self.brand_profile.name} | {self.insta_count} | {self.fb_count}"
