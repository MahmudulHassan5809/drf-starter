import json
import logging
import random
import jwt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from accounts.utils.token import create_tokens

from base.exceptions import UnprocessableEntity
from base.helpers.decorators import exception_handler
from accounts.models import User
from accounts.serializers import UserSerializer
from accounts.tasks.users import send_sms
from base.cache.redis_cache import delete_cache, get_cache, set_cache

logger = logging.getLogger('django')


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request: Request) -> Response:
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        raise ValidationError(
            detail='username and password if required', code=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(username__exact=username)
        if not user.check_password(raw_password=password):
            raise ValidationError(detail='invalid password',
                                  code=status.HTTP_400_BAD_REQUEST)
        access_token, refresh_token = create_tokens(user=user)
        data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
        set_cache(key=f'{username}_token_data', value=json.dumps(
            UserSerializer(user).data), ttl=5*60*60)
        print(get_cache(f'{username}_token_data'))
        return Response(data=data, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        raise ValidationError(detail='user not found',
                              code=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def refreshed_token(request: Request) -> Response:
    refreshed_token = request.data.get('refresh_token')
    try:
        payload = jwt.decode(
            jwt=refreshed_token, key=settings.SECRET_KEY, algorithms='HS256', verify=True)
        if payload['token_type'] != 'refresh':
            return JsonResponse(data={
                'message': 'no refresh token provided',
                'success': False
            }, status=400)
        user_name = payload.get('username')
        user_obj = get_object_or_404(User, username=user_name)
        if get_cache(f'{user_obj.username}_token_data'):
            raise ValidationError(
                detail='Already have a valid token', code=status.HTTP_401_UNAUTHORIZED)
        if not user_obj.is_active:
            raise ValidationError(
                detail='user is not active', code=status.HTTP_401_UNAUTHORIZED)
        access_token, refresh_token = create_tokens(user=user_obj)
        data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
        return Response(data=data, status=status.HTTP_201_CREATED)
    except Exception as err:
        return JsonResponse(data={
            'message': f'{str(err)}',
            'success': False,
        }, status=401)


@api_view(['POST'])
@permission_classes([AllowAny])
@exception_handler
def reset_password_otp_send(request: Request) -> Response:
    username = request.data['username']
    user = get_object_or_404(User, username=username)

    if not user.contact_number:
        raise UnprocessableEntity(
            detail='User Has no contact number!', code=status.HTTP_406_NOT_ACCEPTABLE)
    if not settings.DEBUG:
        otp = random.randint(10000, 99999)
    else:
        otp = 99999
    if not set_cache(key=f'{user.username}_otp', value=str(otp), ttl=300):
        raise ValidationError(detail='otp not set',
                              code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    send_sms(username=user.contact_number, message=f'your otp is {otp}')
    return Response(data={'Message': "An Otp sent to your contact no! Please get it and verify your account!"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
@exception_handler
def reset_password_verify_otp(request: Request) -> Response:
    username = request.data['username']
    try:
        user = User.objects.get(username=username)
        otp = get_cache(f'{user.username}_otp')
        if not otp:
            raise ValidationError('cannot get otp value',
                                  code=status.HTTP_404_NOT_FOUND)
        if otp != request.data['otp']:
            raise ValidationError('otp does not match',
                                  code=status.HTTP_400_BAD_REQUEST)
        delete_cache(f'{user.username}_otp')
        password = request.data['password']
        user.set_password(raw_password=password)
        user.save()
        return Response({'message': f'{user.username}"s password changed successfully!'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        raise ValidationError(detail='user does not exists',
                              code=status.HTTP_404_NOT_FOUND)
