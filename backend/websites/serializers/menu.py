# serializers/menu.py
from rest_framework import serializers
from websites.models.menu import Menu
from base.serializers import WritableNestedSerializer
from base.serializers.recursive import RecursiveSerializer
from contents.serializers import ShortContentSerializer


class MenuSerializer(WritableNestedSerializer):
    title = ShortContentSerializer(required=False)
    parent_id = serializers.UUIDField(required=False, allow_null=True)
    site_id = serializers.UUIDField(required=False, allow_null=True)

    class Meta:
        model = Menu
        fields = [
            "id",
            "title",
            "parent_id",
            "url",
            "order",
            "site_id",
            "created_at",
            "updated_at"
        ]
        extra_kwargs = {
            "title": {"required": False},
            "url": {"required": False, "allow_null": True},
            "order": {"required": False},
        }
        read_only_fields = ["id", "created_at", "updated_at"]
        nested_create_fields = ["title"]
        nested_update_fields = ["title"]


class MenuTreeSerializer(serializers.ModelSerializer):
    parent_id = serializers.UUIDField(required=False, allow_null=True)
    site_id = serializers.UUIDField(required=False, allow_null=True)
    children = RecursiveSerializer(many=True, required=False)

    class Meta:
        model = Menu
        fields = [
            "id",
            "title",
            "parent_id",
            "url",
            "order",
            "children",
            "site_id",
            "created_at",
            "updated_at"
        ]
        extra_kwargs = {
            "label": {"required": True},
            "url": {"required": False, "allow_null": True},
            "order": {"required": False},
        }
        read_only_fields = ["id", "created_at", "updated_at"]
        nested_create_fields = ["title"]
        nested_update_fields = ["title"]
