from rest_framework import serializers
from rest_framework.fields import UUIDField
from base.serializers import WritableNestedSerializer
from ..models import Namespace, HomePage

class HomePageSerializer(WritableNestedSerializer):
    namespace_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Namespace.objects.all(),
        source='namespace'
    )

    class Meta:
        model = HomePage
        fields = [
            "id",
            "namespace_id",
            "content",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at"
        ]
        
        extra_kwargs = {
            'content': {'required': False}
        }

        read_only_fields = ["id", "created_by", "created_at", "updated_by", "updated_at"]