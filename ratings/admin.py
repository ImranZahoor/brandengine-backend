from django.contrib import admin
from .models import Ratings


@admin.register(Ratings)
class RatingsAdmin(admin.ModelAdmin):
    list_display = ["user", "rating", "brand_profile", "created_at"]
