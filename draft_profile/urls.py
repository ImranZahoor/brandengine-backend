from django.urls import path, include
from rest_framework.routers import DefaultRouter

from draft_profile.views import DraftProfileViewSet, UploadCSVView, MigrateBrands

app_name = "draft"
router = DefaultRouter()
router.register("draft_profile", DraftProfileViewSet, basename="draft_profile")

urlpatterns = [
    path("", include(router.urls)),
    path("draft_profile/upload", UploadCSVView.as_view(), name="upload_csv_draft"),
    path("migrate_profile/", MigrateBrands.as_view(), name="migrate"),
]
