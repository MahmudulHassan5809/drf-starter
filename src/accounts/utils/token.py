import datetime
from typing import Tuple
import jwt
from django.conf import settings
from accounts.models import User


def generate_access_token(user: User) -> str:
    token_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'is_active': user.is_active,
        'is_superuser': user.is_superuser,
        'is_staff': user.is_staff,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=5),
        'token_type': 'access'
    }
    raw_token = jwt.encode(
        payload=token_data, key=settings.SECRET_KEY, algorithm='HS256',)
    # token = raw_token.decode('utf-8')
    return raw_token


def generate_refresh_token(user: User) -> str:
    token_data = {
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=1),
        'token_type': 'refresh'
    }
    raw_token = jwt.encode(
        payload=token_data, key=settings.SECRET_KEY, algorithm='HS256')
    # token = raw_token.decode('utf-8')
    return raw_token


def create_tokens(user: User) -> Tuple[str, str]:
    return generate_access_token(user=user), generate_refresh_token(user=user)
