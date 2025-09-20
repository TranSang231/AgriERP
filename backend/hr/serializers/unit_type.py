from ..models.unit_type import UnitType
from rest_framework import serializers



class UnitTypeSerializer(serializers.ModelSerializer):
    business_id = serializers.UUIDField(required=False, allow_null=True)      
    class Meta:         
        model = UnitType
        fields = ["id", "name", "description","business_id","created_at","updated_at"]
        extra_kwargs = {
            "id": {"required": False, "read_only": False, "allow_null": True},
            'name': {'required': True},
            'description': {'required': False, "allow_null": True},
        }