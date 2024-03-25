from django.contrib import admin
from brandusers.models import BrandUser


class BrandUserAdmin(admin.ModelAdmin):
    ordering = ("user",)
    list_display = ("user",)
    search_fields = ("user",)
    filter_horizontal = ()
    # list_filter = ("is_brand", "is_active", "is_staff", "is_superuser")


admin.site.register(BrandUser, BrandUserAdmin)
