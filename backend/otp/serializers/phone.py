from rest_framework import serializers
from ..models import PhoneOTPDevice


class PhoneOTPDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneOTPDevice
        fields = [
            'id',
            'name',
            'phone',
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

