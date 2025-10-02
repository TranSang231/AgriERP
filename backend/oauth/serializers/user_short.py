from ..models import User
from rest_framework import serializers

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "active",
        ]
        depth = 1
