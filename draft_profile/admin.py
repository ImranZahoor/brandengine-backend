from django.contrib import admin
from draft_profile.models import DraftProfile


@admin.register(DraftProfile)
class DraftProfileAdmin(admin.ModelAdmin):
    list_display = ["brand_name", "category", "url", "title"]
    list_filter = ["title", "brand_name"]
    search_fields = ["title", "brand_name"]
