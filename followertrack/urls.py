from django.urls import path, include
from rest_framework.routers import DefaultRouter

from followertrack.views import FollowerTrackViewSet

app_name = "follower_track"
router = DefaultRouter()
router.register("follower_track", FollowerTrackViewSet, basename="follower_track")

urlpatterns = [
    path("", include(router.urls)),
]
