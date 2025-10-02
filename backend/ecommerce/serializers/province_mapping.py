from rest_framework import serializers
from rest_framework.fields import UUIDField
from ..models import Province, DeliveryServiceProvider, ProvinceMapping

class ProvinceMappingSerializer(serializers.ModelSerializer):
    province_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Province.objects.all(),
        pk_field=UUIDField(format='hex'),
        source='province'
    )
    delivery_service_provider_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=DeliveryServiceProvider.objects.all(),
        pk_field=UUIDField(format='hex'),
        source='delivery_service_provider'
    )

    class Meta:
        model = ProvinceMapping
        fields = [
            "id",
            "province_id",
            "delivery_service_provider_id",
            "data",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            'data': {'required': False}
        }
        read_only_fields = ["id", "created_at", "updated_at"]