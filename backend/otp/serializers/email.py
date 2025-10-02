from rest_framework import serializers
from ..models import EmailOTPDevice


class EmailOTPDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailOTPDevice
        fields = [
            'id',
            'name',
            'email',
            'confirmed',
            'token',
            'valid_until',
            'last_generated_timestamp',
            'throttling_failure_timestamp',
            'throttling_failure_count',
            'created_at',
            'last_used_at'
        ]
        extra_kwargs = {
            'name': {'required': False},
            'confirmed': {'required': False},
            'token': {'required': False},
            'valid_until': {'required': False},
            'last_generated_timestamp': {'required': False},
            'throttling_failure_timestamp': {'required': False},
            'created_at': {'required': False},
            'last_used_at': {'required': False},
        }
        depth = 1

