from django.contrib import admin
from .models import FollowerTrack


@admin.register(FollowerTrack)
class FollowerTrackAdmin(admin.ModelAdmin):
    list_display = ("brand_profile", "insta_count", "fb_count")
    list_filter = ("brand_profile",)
    search_fields = ("brand_profile__name",)
