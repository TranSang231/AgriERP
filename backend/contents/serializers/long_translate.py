from rest_framework import serializers
from ..models import LongTranslate
class LongTranslateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongTranslate
        fields = ['id', 'language', 'value']