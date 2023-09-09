from accounts.views.user import UserProfileRetrieveView, logout, user_password_change
from django.urls import path

app_name = "user"

urlpatterns = [
    path("profile/", UserProfileRetrieveView.as_view(), name="user_profile_get"),
    path("password-change/", user_password_change, name="user_password_change"),
    path("logout/", logout, name="user_logout"),
]
