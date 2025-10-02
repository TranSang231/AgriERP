from django.contrib.auth import get_user_model
from rest_framework import serializers
from oauth.serializers import UserShortSerializer
from ..models import Namespace

User = get_user_model()


class NamespaceShortSerializer(serializers.ModelSerializer):
    owner = UserShortSerializer(required=False, read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=User.objects.all(),
        source='owner'
    )

    class Meta:
        model = Namespace
        fields = [
            "id",
            "name",
            "slug",
            "logo",
            "description",
            "access",
            "owner",
            "owner_id",
            "created_at",
            "updated_at"
        ]
        
        extra_kwargs = {
            'name': {'required': False},
            'slug': {'required': False},
            'logo': {'required': False},
            'description': {'required': False},
            'access': {'required': False}
        }

        read_only_fields = ["id", "created_at", "updated_at"]