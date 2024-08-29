from django.urls import path, include
from rest_framework.routers import DefaultRouter

from ratings.views import RatingsViewSet,UserRatingsViewSet

app_name = "rating"
router = DefaultRouter()
router.register("rating", RatingsViewSet, basename="ratings")
router.register(r'user-ratings', UserRatingsViewSet, basename='user-ratings')

urlpatterns = [
    path("", include(router.urls)),
]
