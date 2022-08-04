from django.urls import path


from accounts.views.admin import (
    AdminUserListCreateApiView
)

app_name = 'admin'

urlpatterns = [
    path('users/', AdminUserListCreateApiView.as_view(),
         name='user_list_create'),

]
