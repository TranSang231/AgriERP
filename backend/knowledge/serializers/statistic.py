from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Namespace, Page


class GeneralStatisticSerializer(serializers.Serializer):
    """General Statistics information"""

    total_users = serializers.IntegerField()
    total_namespaces = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    time = serializers.DateTimeField()


class PagesCountByDateSerializer(serializers.Serializer):
    """Serializer for pages created/updatated by date"""
    
    date = serializers.DateField()
    count = serializers.IntegerField()