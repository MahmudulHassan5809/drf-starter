from django.contrib.auth import get_user_model
from rest_framework.serializers import Serializer
from rest_framework.fields import CharField
from base.serializers import DynamicFieldsModelSerializer


User = get_user_model()


class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username',
                  'email', 'is_active',)


class ChangePasswordSerializer(Serializer):
    old_password = CharField(required=True)
    new_password = CharField(required=True)
