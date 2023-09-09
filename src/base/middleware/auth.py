from typing import Union

import jwt
from accounts.models import User
from django.http import HttpRequest, JsonResponse
from myproject.settings import SECRET_KEY
from rest_framework.exceptions import ValidationError


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def get_user(data: dict) -> Union[User, object]:
        try:
            try:
                user_data = User.objects.get(username=data.get("username"))
            except Exception:
                raise ValidationError(detail="user data not found", code=401)
            user = user_data
            if not user.is_active:
                return
            return user
        except User.DoesNotExist:
            return

    def __call__(self, request: HttpRequest):
        request._dont_enforce_csrf_checks = True
        auth_header: str = request.headers.get("authorization")
        if auth_header:
            token_obj: list[str] = auth_header.split(" ")
            if token_obj[0].lower() != "bearer":
                return JsonResponse(
                    data={
                        "message": "invalid token type",
                        "success": False,
                    },
                    status=400,
                )
            try:
                payload: dict = jwt.decode(
                    jwt=token_obj[1], key=SECRET_KEY, algorithms="HS256", verify=True
                )
                if payload["token_type"] != "access":
                    return JsonResponse(
                        data={"message": "no access token provided", "success": False},
                        status=400,
                    )
                user_obj = self.get_user(data=payload)
                if not user_obj:
                    return JsonResponse(
                        data={
                            "message": "cannot retrieve user information",
                            "success": False,
                        },
                        status=401,
                    )
                request.user = user_obj
            except Exception as err:
                return JsonResponse(
                    data={
                        "message": f"{str(err)}",
                        "success": False,
                    },
                    status=401,
                )
        response = self.get_response(request)
        return response
