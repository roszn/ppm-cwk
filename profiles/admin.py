from django.contrib import admin
from .models import EmployeeProfile

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'job_role', 'department', 'line_manager']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'job_role', 'department']
    list_filter = ['department']
