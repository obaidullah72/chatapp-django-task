# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("profile/", views.profile_page, name="profile-page"),
    # add more (signup, settings, etc.) later
]
