from django.contrib import admin
from django.urls import path, include
from .views import home 
from .views import signup_view 
from users.views import CustomLoginView, CustomLogoutView

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    path("chat/", include("chat.urls")),

    # Custom Auth
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path('signup/', signup_view, name='signup'),
]
