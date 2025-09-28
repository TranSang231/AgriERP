from rest_framework import serializers
from rest_framework.fields import UUIDField
from base.serializers import WritableNestedSerializer
from ..models import Customer
from oauth.models import User
from oauth.serializers import UserShortSerializer
from .shipping_address import ShippingAddressSerializer

class CustomerSerializer(WritableNestedSerializer):
    user = UserShortSerializer(required=False)
    user_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=User.objects.all(),
                                                       pk_field=UUIDField(format='hex'), source='user')
    shipping_addresses = ShippingAddressSerializer(many=True, required=False)

    class Meta:
        model = Customer
        fields = [
            'id',
            'user',
            'user_id',
            'email',
            'first_name',
            'last_name',
            'phone',
            'address',
            'date_of_birth',
            'gender',
            'status',
            'shipping_addresses',
            'created_at',
            'updated_at'
        ]
        extra_kwargs = {
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone': {'required': False},
            'address': {'required': False},
            'date_of_birth': {'required': False},
            'gender': {'required': False},
            'status': {'required': False}
        }
        read_only_fields = ["id", "created_at", "updated_at"]
        nested_create_fields = ["user"]

