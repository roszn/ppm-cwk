from django.contrib import admin
from .models import HolidayRequest, HolidayAllowance


@admin.register(HolidayRequest)
class HolidayRequestAdmin(admin.ModelAdmin):
    list_display = ['employee', 'request_type', 'start_date', 'end_date', 'working_days', 'status', 'reviewed_by']
    list_filter = ['status', 'request_type']
    search_fields = ['employee__email', 'employee__first_name', 'employee__last_name']


@admin.register(HolidayAllowance)
class HolidayAllowanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'year', 'total_days']
    search_fields = ['employee__email']
