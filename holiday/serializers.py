from rest_framework import serializers
from .models import HolidayRequest, HolidayAllowance


class HolidayRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    reviewed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = HolidayRequest
        fields = [
            'id', 'employee_name', 'request_type', 'absence_reason',
            'start_date', 'end_date', 'working_days', 'notes',
            'status', 'reviewed_by_name', 'reviewed_at', 'created_at',
        ]
        read_only_fields = ['id', 'employee_name', 'working_days', 'status', 'reviewed_by_name', 'reviewed_at', 'created_at']

    def get_employee_name(self, obj):
        name = f"{obj.employee.first_name} {obj.employee.last_name}".strip()
        return name or obj.employee.email

    def get_reviewed_by_name(self, obj):
        if obj.reviewed_by:
            name = f"{obj.reviewed_by.first_name} {obj.reviewed_by.last_name}".strip()
            return name or obj.reviewed_by.email
        return None

    def validate(self, data):
        start = data.get('start_date')
        end = data.get('end_date')
        if start and end and end < start:
            raise serializers.ValidationError("End date cannot be before start date.")
        return data


class HolidayAllowanceSerializer(serializers.ModelSerializer):
    days_approved = serializers.SerializerMethodField()
    days_pending = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()

    class Meta:
        model = HolidayAllowance
        fields = ['year', 'total_days', 'days_approved', 'days_pending', 'days_remaining']

    def get_days_approved(self, obj):
        return obj.days_approved()

    def get_days_pending(self, obj):
        return obj.days_pending()

    def get_days_remaining(self, obj):
        return obj.days_remaining()
