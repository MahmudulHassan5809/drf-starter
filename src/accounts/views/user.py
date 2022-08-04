from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from base.cache.redis_cache import delete_cache
from accounts.serializers import ChangePasswordSerializer, UserSerializer


User = get_user_model()


class UserProfileRetrieveView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.filter()
    http_method_names = ['get', 'patch']
    swagger_tags = ["User Profile"]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        # delete_cache(f'{request.user.username}_token_data')
        return super().patch(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_password_change(request: Request) -> Response:
    user = request.user
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        if not user.check_password(serializer.data.get("old_password")):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.data.get("new_password"))
        user.save()
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Password updated successfully',
            'data': []
        }
        # delete_cache(f'{request.user.username}_token_data')
        return Response(response)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def logout(request: Request) -> Response:
    if not request.user:
        raise ValidationError(detail='user not found',
                              code=status.HTTP_404_NOT_FOUND)
    delete_cache(f'{request.user.username}_token_data')
    return Response(data={'message': 'user has been logged out'}, status=status.HTTP_200_OK)
