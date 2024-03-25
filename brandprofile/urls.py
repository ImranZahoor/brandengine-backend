from django.urls import path, include
from rest_framework.routers import DefaultRouter

from brandprofile.views import BrandProfileViewSet, CategoryViewSet, UploadCSVView

app_name = "profile"
router = DefaultRouter()
router.register("profile", BrandProfileViewSet, basename="profile")
router.register("category", CategoryViewSet, basename="category")

urlpatterns = [
    path("", include(router.urls)),
    path("brand/upload", UploadCSVView.as_view(), name="upload_csv"),
]
