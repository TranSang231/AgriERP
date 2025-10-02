from rest_framework import serializers
from rest_framework.fields import UUIDField

from base.serializers import WritableNestedSerializer
from oauth.serializers import UserShortSerializer

from oauth.models import User
from ..models import UserToken


class UserTokenSerializer(WritableNestedSerializer):
    user = UserShortSerializer(required=False)
    user_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=User.objects.all(),
                                                 pk_field=UUIDField(format='hex'), source='user')

    class Meta:
        model = UserToken
        fields = ['id', 'user', 'user_id', 'token']
