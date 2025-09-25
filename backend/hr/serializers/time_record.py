from rest_framework import serializers

from hr.models.time_record import TimeRecord


class TimeRecordSerializer(serializers.ModelSerializer):
    employee_id = serializers.UUIDField(write_only=True)
    office_id = serializers.UUIDField(required=False, allow_null=True, write_only=True)

    class Meta:
        model = TimeRecord
        fields = [
            'id',
            'employee_id',
            'office_id',
            'check_in_at',
            'check_out_at',
            'duration_seconds',
            'source',
            'note',
            'created',
            'modified',
        ]
        read_only_fields = ['duration_seconds', 'created', 'modified']

    def create(self, validated_data):
        employee_id = validated_data.pop('employee_id')
        office_id = validated_data.pop('office_id', None)
        validated_data['employee_id'] = employee_id
        if office_id:
            validated_data['office_id'] = office_id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Prevent changing ownership
        validated_data.pop('employee_id', None)
        validated_data.pop('office_id', None)
        return super().update(instance, validated_data)



