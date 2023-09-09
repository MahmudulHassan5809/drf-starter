from accounts.models import User

SUPERUSER_USERNAME = "admin"
SUPERUSER_EMAIL = "admin@gmail.com"
SUPERUSER_PASSWORD = "admin"
EXTRA = {"is_active": True, "phone_number": "01630811624"}


def run():
    User.objects.create_superuser(
        SUPERUSER_USERNAME, SUPERUSER_EMAIL, SUPERUSER_PASSWORD, **EXTRA
    )
    return
