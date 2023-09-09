from accounts.models import User
from django.contrib.auth.hashers import make_password
from faker import Faker


def get_fake_profiles(count=10):
    fake = Faker()
    user_data = []
    for _ in range(count):
        profile = fake.profile()
        data = {
            "username": profile.get("username"),
            "email": profile.get("mail"),
            "is_active": True,
            "password": make_password(fake.password(length=15)),
            "phone_number": fake.phone_number(),
        }
        if "name" in profile:
            fname, lname = profile.get("name").split(" ")[:2]
            data["first_name"] = fname
            data["last_name"] = lname

        user_data.append(data)
    return user_data


def run():
    user_data = get_fake_profiles(count=10)
    User.objects.bulk_create([User(**user) for user in user_data])
    return
