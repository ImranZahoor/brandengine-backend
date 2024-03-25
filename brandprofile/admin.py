from django.contrib import admin
from .models import Category, BrandProfile, BrandLocation

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']

@admin.register(BrandProfile)
class BrandProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'website', 'country']
    list_filter = ['category', 'country']
    search_fields = ['name', 'country']

@admin.register(BrandLocation)
class BrandLocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'brand', 'address', 'city', 'country']
    list_filter = ['city', 'country']
    search_fields = ['brand__name', 'city', 'country']
