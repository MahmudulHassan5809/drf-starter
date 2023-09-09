from accounts.filters import UserFilter
from accounts.serializers import UserSerializer
from base.helpers.decorators import exception_handler
from base.permissions import IsStaff, IsSuperUser
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class AdminUserListCreateApiView(ListCreateAPIView):
    permission_classes = (
        IsAuthenticated,
        (IsStaff | IsSuperUser),
    )
    serializer_class = UserSerializer
    queryset = User.objects.filter()
    filterset_class = UserFilter
    swagger_tags = ["Users"]

    @method_decorator(exception_handler)
    def create(self, request, *args, **kwargs):
        request.data["is_active"] = True
        request.data["password"] = make_password(request.data["password"])
        return super().create(request, *args, **kwargs)
