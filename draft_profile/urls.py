from django.urls import path, include
from rest_framework.routers import DefaultRouter

from draft_profile.views import DraftProfileViewSet, UploadCSVView, MigrateBrands

app_name = "draft"
router = DefaultRouter()
router.register("draft_profile", DraftProfileViewSet, basename="draft_profile")

urlpatterns = [
    path("", include(router.urls)),
    path("draft_profile/upload", UploadCSVView.as_view(), name="upload_csv_draft"),
    path(
        "draft_profile/migrate",
        DraftProfileViewSet.as_view({"post": "migrate_brands"}),
        name="migrate_draft_profile",
    ),
    # path("draft_profile/migrate", MigrateBrands.as_view(), name="migrate"),
]
