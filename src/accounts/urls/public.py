from django.urls import path


from accounts.views.public import (
    login,
    refreshed_token,
    reset_password_otp_send,
    reset_password_verify_otp,
)

app_name = 'public'

urlpatterns = [
    path('login/', login, name='user_login_api'),
    path('refresh-token/', refreshed_token, name='user_token_refresh_api'),
    path('pass-reset-otp/', reset_password_otp_send,
         name='user-pass-reset-otp-send-api'),
    path('pass-reset/', reset_password_verify_otp, name='user_pass_reset_api'),
]
