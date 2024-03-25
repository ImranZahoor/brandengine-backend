from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ratings.views import RatingsViewSet

app_name = "rating"
router = DefaultRouter()
router.register("rating", RatingsViewSet, basename="ratings")

urlpatterns = [
    path("", include(router.urls)),
]
