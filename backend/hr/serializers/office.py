from rest_framework import serializers
from rest_framework.fields import UUIDField
from hr.models.holiday import Holiday
from base.serializers.writable_nested import WritableNestedSerializer
from hr.serializers.work_session import WorkSessionSerializer
from ..models import Office
from .holiday import HolidaySerializer
from businesses.serializers.employee import EmployeeShortSerializer

class OfficeSerializer(WritableNestedSerializer):
    business_id = UUIDField(required=False, allow_null=True)
    manager_id = UUIDField(required=False, allow_null=True)
    manager = EmployeeShortSerializer(required=False,read_only=True)
    group_id = UUIDField(required=False, allow_null=True)
    holidays = HolidaySerializer(many=True, required=False)
    sessions = WorkSessionSerializer(many=True, required=False)
    employees = EmployeeShortSerializer(many=True,required =False)
    class Meta:
        model = Office
        fields = [
            "id",
            "name",
            "email",
            "address",
            "phone",
            "established_date",
            "remain_leaves_period",
            "business_id",
            "manager_id",
            "manager",
            "group_id",
            "holidays",
            "sessions",
            "employees",
        ]
        extra_kwargs = {
            'name': {'required': False},
            'email': {'required': False},  
            'address': {'required': False},
        }

    def _update_holidays(self, office, holidays_data):
        # Clear existing holidays
        office.holidays.all().delete()
        # Add new holidays
        new_holidays = [Holiday(office=office, **holiday) for holiday in holidays_data]
        Holiday.objects.bulk_create(new_holidays)


class OfficeShortSerializer(serializers.ModelSerializer):
    business_id = UUIDField(required=False, allow_null=True)
    manager_id = UUIDField(required=False, allow_null=True)
    group_id = UUIDField(required=False, allow_null=True)
    work_sessions = WorkSessionSerializer(many=True, required=False)
    class Meta:
        model = Office
        fields = [
            "id",
            "business_id",
            "manager_id",
            "group_id",
            "name",
            "email",
            "address",
            "phone",
            "established_date",
            "remain_leaves_period",
            "work_sessions",
        ]
        extra_kwargs = {
            'name': {'required': False},
            'email': {'required': False},
            'address': {'required': False},
        }
