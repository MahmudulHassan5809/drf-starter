from accounts.views.admin import AdminUserListCreateApiView
from django.urls import path

app_name = "admin"

urlpatterns = [
    path("users/", AdminUserListCreateApiView.as_view(), name="user_list_create"),
]
