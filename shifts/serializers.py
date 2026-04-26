from rest_framework import serializers
from holiday.models import HolidayRequest
from .models import BankHoliday, Shift


class BankHolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = BankHoliday
        fields = ['id', 'name', 'date']


class ShiftSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = Shift
        fields = ['id', 'employee', 'employee_name', 'date', 'start_time', 'end_time']

    def get_employee_name(self, obj):
        name = f"{obj.employee.first_name} {obj.employee.last_name}".strip()
        return name or obj.employee.email


class CalendarHolidaySerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()

    class Meta:
        model = HolidayRequest
        fields = [
            'id', 'employee_name', 'request_type', 'absence_reason',
            'start_date', 'end_date', 'working_days', 'status',
        ]

    def get_employee_name(self, obj):
        name = f"{obj.employee.first_name} {obj.employee.last_name}".strip()
        return name or obj.employee.email
