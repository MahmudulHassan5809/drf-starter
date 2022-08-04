from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from accounts.filters import UserFilter
from base.helpers.decorators import exception_handler
from base.permissions import IsStaff, IsSuperUser
from accounts.serializers import UserSerializer


User = get_user_model()


class AdminUserListCreateApiView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser),)
    serializer_class = UserSerializer
    queryset = User.objects.filter()
    filterset_class = UserFilter
    swagger_tags = ["Firm User"]

    @method_decorator(exception_handler)
    def create(self, request, *args, **kwargs):
        request.data['is_active'] = True
        request.data['password'] = make_password(request.data['password'])
        return super(AdminUserListCreateApiView, self).create(request, *args, **kwargs)
