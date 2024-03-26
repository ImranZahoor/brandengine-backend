"""
URL configuration for brand project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from users.views import (
    CustomRegisterView,
    CustomLoginView,
    FacebookLogin,
    InstagramLogin,
)
from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView

urlpatterns = [
    path("api/auth/", include("dj_rest_auth.urls")),
    path("accounts/", include("allauth.urls")),
    path("api/auth/registration", CustomRegisterView.as_view(), name="register"),
    path("api/auth/login", CustomLoginView.as_view(), name="rest_login"),
    path("api/auth/password/reset", PasswordResetView.as_view(), name="rest_login"),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path(
        "api/auth/password/reset/confirm/<str:uidb64>/<str:token>",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("api/dj-rest-auth/facebook/", FacebookLogin.as_view(), name="fb_login"),
    path("api/dj-rest-auth/instagram/", InstagramLogin.as_view(), name="insta_login"),
    path("api/users/", include("users.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("ratings.urls")),
    path("api/", include("followertrack.urls")),
    path("api/", include("brandprofile.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Brand Search Engine"
admin.site.site_title = "Brand Search Engine Admin Portal"
admin.site.index_title = "Welcome to Brand Search Engine Admin Portal"
