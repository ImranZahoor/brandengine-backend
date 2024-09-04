from django.urls import path
from .views import PostContact

urlpatterns = [
    path('contact_us/', PostContact.as_view(), name='subscribe'),
]