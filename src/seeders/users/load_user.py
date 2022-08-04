from accounts.models import User
from seeders.users.factories import UserFactory

NUM_USER = 100


def run():
    print("------------ Load user data -------------")

    User.objects.all().delete()

    # Add user
    for _ in range(NUM_USER):
        UserFactory()

    print("------------ End user data -------------")
    return
