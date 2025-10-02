from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from hr.models.office import Office
from ..models import WorkSession


class WorkSessionSerializer(serializers.ModelSerializer):
    office_id=serializers.PrimaryKeyRelatedField(required=False, write_only=True, queryset=Office.objects.all(),
                                                   source='office')

    class Meta:
        model = WorkSession
        fields = ["id","start_time","end_time","work_day","office_id","created_at","updated_at"]

    def validate(self, attrs):
        start_time = attrs.get("start_time", None)
        end_time = attrs.get("end_time", None)
        work_day = attrs.get("work_day", None)
        office = attrs.get("office", None)
        print("office",office)

        if not (start_time and end_time):
            raise ValidationError({"detail": "start_time/end_time is missing"})
        if start_time >= end_time:
            raise ValidationError({"detail": "start_time must before end_time"})
        if work_day is None:
            raise ValidationError({"detail": "work_day is missing"})
        if office is None:
            raise ValidationError({"detail": "office is missing"})
        self.check_overlapping(attrs)       
        return attrs

    def create(self, validated_data):
        # self.check_overlapping(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # self.check_overlapping(validated_data, instance.id)
        return super().update(instance, validated_data)
    
    def check_overlapping(self, validated_data, session_id=None):
        start_time = validated_data.get("start_time")
        end_time = validated_data.get("end_time")
        work_day = validated_data.get("work_day")
        office = validated_data.get("office")

        overlapping_sessions = WorkSession.objects.exclude(id=session_id).filter(
            Q(work_day=work_day),
            Q(office=office),
            Q(start_time__gte=start_time, start_time__lt=end_time)
            | Q(end_time__gt=start_time, end_time__lte=end_time),
        )
        if overlapping_sessions.exists():
            raise ValidationError({"detail": "time range is overlapping"})
