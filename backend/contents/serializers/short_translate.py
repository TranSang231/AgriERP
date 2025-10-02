from rest_framework import serializers
from ..models import ShortTranslate

class ShortTranslateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortTranslate
        fields = ['id', 'language', 'value']