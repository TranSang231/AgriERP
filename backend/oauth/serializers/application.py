from rest_framework import serializers
from ..models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            "id",
            "client_id",
            "client_secret",
            "user",
            "redirect_uris",
            "post_logout_redirect_uris",
            "client_type",
            "authorization_grant_type",
            "name",
            "skip_authorization",
            "algorithm",
            "scope",
            "type",
            "created",
            "updated"
        ]
        extra_kwargs = {
            "user": {"required": False},
            "name": {"required": False},
            "client_secret": {"required": False, "write_only": True},
            "redirect_uris": {"required": False},
            "post_logout_redirect_uris": {"required": False},
            "scope": {"required": False},
            "created": {"required": False, "read_only": True},
            "updated": {"required": False, "read_only": True}
        }
