from django.contrib.auth import get_user_model
from rest_framework import serializers
from base.serializers import WritableNestedSerializer
from oauth.serializers import UserShortSerializer
from ..models import Namespace
from .namespace_member import NamespaceMemberSerializer

User = get_user_model()

class NamespaceSerializer(WritableNestedSerializer):
    owner = UserShortSerializer(required=False, read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=User.objects.all(),
        source='owner'
    )
    members = NamespaceMemberSerializer(many=True, required=False, source='namespace_memebers')

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
            "members",
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
        nested_create_fields = ["members"]
        nested_update_fields = ["members"]


class NamespaceShortSerializer(serializers.ModelSerializer):
    owner = UserShortSerializer(required=False)

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
            "created_at",
            "updated_at"]
        
        extra_kwargs = {
            'name': {'required': False},
            'slug': {'required': False},
            'logo': {'required': False},
            'description': {'required': False},
            'access': {'required': False}
        }

        read_only_fields = ["id", "created_at", "updated_at"]