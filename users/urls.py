from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, user_detail_view, UserRedirectView

app_name = "users"
router = DefaultRouter()
router.register("", UserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
    path("~redirect/", view=UserRedirectView.as_view(), name="redirect"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
