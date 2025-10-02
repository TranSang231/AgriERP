from rest_framework import serializers
from rest_framework.fields import UUIDField
from ..models import Customer, Province, District, Ward, ShippingAddress
from .province import ProvinceSerializer
from .district import DistrictSerializer
from .ward import WardSerializer

class ShippingAddressSerializer(serializers.ModelSerializer):
    customer_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Customer.objects.all(),
        pk_field=UUIDField(format='hex'),
        source='customer'
    )
    province = ProvinceSerializer(required=False)
    province_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Province.objects.all(),
        pk_field=UUIDField(format='hex'),
        source='province'
    )
    district = DistrictSerializer(required=False)
    district_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=District.objects.all(),
        pk_field=UUIDField(format='hex'),
        source='district'
    )
    ward = WardSerializer(required=False)
    ward_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Ward.objects.all(),
        pk_field=UUIDField(format='hex'),
        source='delivery_service_provider'
    )

    class Meta:
        model = ShippingAddress
        fields = [
            "id",
            "customer_id",
            "province",
            "province_id",
            "district",
            "district_id",
            "ward",
            "ward_id",
            "address",
            "is_default",
            "created_at",
            "updated_at"
        ]
        
        extra_kwargs = {
            'address': {'required': False},
            'is_default': {'required': False}
        }

        read_only_fields = ["id", "created_at", "updated_at"]
        nested_create_fields = ["mapping"]
        nested_update_fields = ["mapping"]
