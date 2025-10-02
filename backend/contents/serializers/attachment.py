from ..models import Attachment, LongContent
from rest_framework import serializers
from rest_framework.fields import UUIDField


class AttachmentSerializer(serializers.ModelSerializer):
    long_content_id = serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=LongContent.objects.all(),
                                                   pk_field=UUIDField(format='hex'), source='lesson')

    class Meta:
        model = Attachment
        fields = ['id', 'file', 'long_content_id', 'mine_type', 'length', 'original_name', 'path']
        extra_kwargs = {
            'long_content': {'required': False, 'write_only': True},
            'path': {'write_only': True},
        }
