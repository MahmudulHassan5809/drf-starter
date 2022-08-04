from django.urls import path, include

app_name = 'accounts'

urlpatterns = [
    path('admin/', include('accounts.urls.admin'), name='admin.api'),
    path('user/', include('accounts.urls.user'), name='user.api'),
    path('public/', include('accounts.urls.public'), name='public.api'),
]
