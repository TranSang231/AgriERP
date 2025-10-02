from rest_framework import serializers
from rest_framework.fields import UUIDField
from ..models import Ward, DeliveryServiceProvider, WardMapping

class WardMappingSerializer(serializers.ModelSerializer):
    ward_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Ward.objects.all(),
        pk_field=UUIDField(format='hex'),
        source='ward'
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
        model = WardMapping
        fields = [
            "id",
            "ward_id",
            "delivery_service_provider_id",
            "data",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            'data': {'required': False}
        }
        read_only_fields = ["id", "created_at", "updated_at"]