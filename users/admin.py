from django.contrib import admin

# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(admin.ModelAdmin):
    ordering = ("email",)
    list_display = ("email", "is_brand", "dob", "is_active", "is_staff", "is_superuser")
    search_fields = ("email",)
    filter_horizontal = ()
    list_filter = ("is_brand", "is_active", "is_staff", "is_superuser")


admin.site.register(User, UserAdmin)
